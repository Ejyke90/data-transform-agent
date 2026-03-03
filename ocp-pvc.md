# Research: Personal Knowledge Assistant Grounding Service
## OpenShift + PVC + Email/Slack Integration — Production Best Practices

---

## Architecture Overview

A production knowledge assistant grounding service (RAG-based) on OpenShift typically follows this pattern:

```
[Email / Slack / Confluence / Docs]
        ↓ (ingest pipeline)
[Document Processor / Chunker]
        ↓
[Embedding Model]
        ↓
[Vector Store] ←→ [PVC or external vector DB]
        ↓
[Retriever Service] ← [User Query]
        ↓
[LLM + Grounded Context]
        ↓
[Response to User]
```

For the specific S3 → PVC sync pattern, the PVC serves as a local cache of embeddings to avoid
S3 latency on every query and reduce egress costs.

---

## 1. PVC Design Patterns on OpenShift

### Access Mode Selection
| Scenario | Access Mode | StorageClass |
|---|---|---|
| Single sync pod, multiple read pods | ReadWriteMany (RWX) | `ocs-storagecluster-cephfs` (Ceph FS) |
| Single pod (sync + serve) | ReadWriteOnce (RWO) | Any block storage |
| Read-only after sync | ReadOnlyMany (ROX) | After initial write |

**Best practice**: Use `ReadWriteMany` with CephFS for multi-replica services. This allows
one pod to write (sync from S3) while others read (serve embeddings).

### Dedicated Sync Sidecar Pattern
```yaml
# Preferred pattern for OpenShift: sync sidecar + main container share a PVC
spec:
  containers:
  - name: embedding-server        # reads from PVC
    volumeMounts:
    - name: embeddings-pvc
      mountPath: /data/embeddings
      readOnly: true

  - name: s3-sync-sidecar         # writes to PVC on schedule
    volumeMounts:
    - name: embeddings-pvc
      mountPath: /data/embeddings
      readOnly: false

  volumes:
  - name: embeddings-pvc
    persistentVolumeClaim:
      claimName: embeddings-pvc
```

**Why sidecar over init container**: Init containers run once at startup. A sidecar can
run the 15-minute refresh loop continuously alongside the main service.

### Atomic File Swap (avoid read during write corruption)
Never overwrite files in-place during sync. Use a staging directory:
```
/data/embeddings/active/     ← server reads from here
/data/embeddings/staging/    ← sync writes here
```
After sync completes, swap: `mv /data/embeddings/staging /data/embeddings/active-new && 
mv /data/embeddings/active /data/embeddings/active-old && 
mv /data/embeddings/active-new /data/embeddings/active`

---

## 2. S3 → PVC Sync Best Practices

### Change Detection Strategy (priority order)
1. **ETag comparison** — fastest, S3-native, works for single-part uploads
2. **Content MD5/SHA256** — reliable for multipart uploads where ETag ≠ MD5
3. **Last-modified timestamp** — unreliable across regions/clock skew, avoid as primary
4. **File size comparison** — use as secondary check only

### Recommended: Use `aws s3 sync` semantics
If writing custom sync logic, replicate the behavior of `aws s3 sync`:
- List S3 objects with ETags
- Compare against local file ETags (store in a `.sync-manifest.json` on PVC)
- Download only if ETag differs or file is absent
- Update manifest after successful download

### Sync Manifest Pattern
```json
{
  "synced_at": "2026-03-02T23:00:00Z",
  "files": {
    "embeddings/model_v2.faiss": {
      "etag": "d41d8cd98f00b204e9800998ecf8427e",
      "size": 104857600,
      "synced_at": "2026-03-02T22:45:00Z"
    }
  }
}
```
Store this as `/data/embeddings/.sync-manifest.json` on the PVC.

---

## 3. Email & Slack Integration (Grounding Sources)

### Ingestion Architecture
```
Slack API (RTM/Events) ──→ Ingestion Service ──→ Chunker ──→ Embedder ──→ PVC/Vector DB
Gmail/Exchange API ──────→ Ingestion Service ──→ Chunker ──→ Embedder ──→ PVC/Vector DB
```

### Key Considerations

**Slack**:
- Use Slack Events API (webhook-based, not polling) for real-time ingestion
- Scope: `channels:history`, `files:read`, `users:read`
- Rate limit: Tier 3 = 50 req/min. Buffer in a queue (Kafka, RabbitMQ) before embedding
- Filter: Only index messages with reactions or from specific channels (reduce noise)

**Email (Gmail / Exchange)**:
- Use push notifications (Gmail Pub/Sub or Exchange streaming) over polling
- Strip HTML, signatures, and quoted reply chains before chunking
- PII consideration: emails likely contain PII — apply redaction before indexing

### Chunking Strategy for Conversations
- Slack threads: treat the thread as one document (preserve context)
- Emails: subject + body as one chunk; long emails split at paragraph boundaries
- Chunk size: 256–512 tokens with 10–15% overlap is standard for conversational data

---

## 4. Vector Store Options on OpenShift

| Option | Type | OpenShift Support | Notes |
|---|---|---|---|
| **pgvector** (PostgreSQL) | Managed DB | Excellent (Crunchy PGO) | Best for existing Postgres shops |
| **Weaviate** | Dedicated vector DB | Good (Helm chart) | Red Hat has published reference arch |
| **Chroma** | Embedded / server | Good | Lightweight, easy to start |
| **Milvus** | Dedicated vector DB | Good (Operator) | Best for large scale (>100M vectors) |
| **FAISS files on PVC** | File-based | Native (just a PVC) | Your current pattern — good for read-heavy, lower scale |

**For the current ticket (FAISS/files on PVC)**:
- Good choice for <10M vectors and single-model embeddings
- Limitation: FAISS indices are not incrementally updatable — full rebuild on sync
- If incremental updates needed, migrate to pgvector or Weaviate

---

## 5. OpenShift-Specific Production Checklist

### Security
- [ ] S3 credentials in OpenShift `Secret` (not `ConfigMap`)
- [ ] Use IAM role with least privilege (read-only on S3 bucket, no delete)
- [ ] If on AWS, prefer IRSA (IAM Roles for Service Accounts) over static keys
- [ ] NetworkPolicy: restrict sync sidecar egress to S3 endpoints only
- [ ] Slack/email tokens in Secrets, rotated via external-secrets-operator

### Reliability
- [ ] Liveness probe: does NOT depend on sync completion
- [ ] Readiness probe: waits for first sync to complete before serving traffic
- [ ] Sync job must be idempotent (safe to kill and restart at any point)
- [ ] Add `SYNC_LOCK` file or semaphore to prevent concurrent sync runs
- [ ] Alert on sync failures (Prometheus metric: `embedding_sync_last_success_timestamp`)

### Observability
- [ ] Expose Prometheus metrics:
  - `embedding_sync_duration_seconds`
  - `embedding_sync_files_total{status="synced|skipped|failed"}`
  - `embedding_sync_last_success_timestamp`
- [ ] Log structured JSON with fields: `sync_run_id`, `files_checked`, `files_synced`, `files_skipped`
- [ ] Add Grafana dashboard for sync lag (time since last successful sync)

### Resource Sizing (starting point, tune to workload)
```yaml
resources:
  requests:
    cpu: 100m
    memory: 512Mi
  limits:
    cpu: 500m
    memory: 2Gi   # embeddings can be large in memory
```
PVC size: start at 2× the current S3 embedding dataset size (room for staging + active).

---

## 6. Reference Architectures

- **Red Hat + Weaviate RAG on OpenShift**: https://www.redhat.com/en/blog/building-powerful-applications-weaviate-and-red-hat-openshift-retrieval-augmented-generation-workflow
- **Red Hat OpenShift AI Enterprise RAG chatbot**: https://developers.redhat.com/articles/2026/01/29/deploy-enterprise-rag-chatbot-red-hat-openshift-ai
- **RAG in Production — Coralogix**: https://coralogix.com/ai-blog/rag-in-production-deployment-strategies-and-practical-considerations/
- **RAGFlow (open source, self-hosted)**: https://github.com/infiniflow/ragflow
