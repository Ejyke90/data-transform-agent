# Knowledge Assistant — PVC Embedding Sync Prompt
# Usage: Paste into GitHub Copilot Chat or your VS Code AI extension
# Ticket context: Load embeddings from PVC, sync from S3, refresh every 15min, skip unchanged files

---

## PROMPT — PART 1: EMBEDDING LOAD PATH REVIEW

```
Review the codebase and answer the following before suggesting any changes:

1. Where is the S3 client initialized? (file + function + line range)
2. Where are embeddings currently loaded from at runtime? (file + function)
3. Is there an existing scheduler, cron job, or background task runner?
4. Is there any existing file checksum, etag, or modification-time diffing logic?
5. Where is the PVC mount path expected or configured?
6. What is the embedding file format? (.npy, .pkl, .faiss, .bin, other)
7. Are embeddings loaded once at startup or lazily/dynamically?
8. Are there multiple replicas/pods that might all need access to the PVC simultaneously?

Output only findings. No code suggestions yet.
```

---

## PROMPT — PART 2: CONFIG CONTRACT SPEC

```
Before implementation, define the config and data contract changes:

Draft:
1. New environment variables / ConfigMap keys:
   - PVC_MOUNT_PATH (required)
   - S3_BUCKET_NAME (existing or new)
   - S3_EMBEDDING_PREFIX (path prefix in bucket)
   - SYNC_INTERVAL_SECONDS (default 900)
   - EMBEDDING_SOURCE (enum: pvc | s3, default: pvc)

2. Update any internal health/readiness endpoint response schema to include:
   {
     "embedding_source": "pvc",
     "last_sync_at": "<ISO8601>",
     "files_synced": <int>,
     "files_skipped": <int>,
     "sync_status": "ok | syncing | error",
     "sync_error": "<string | null>"
   }

Output OpenAPI YAML or JSON schema only. No implementation code.
```

---

## PROMPT — PART 3: ATOMIC COMMIT PLAN

```
Produce a small, atomic commit plan for these Acceptance Criteria:
- AC1: Load embedding files from PVC (not directly from S3)
- AC2: Copy every file from S3 into PVC
- AC3: Refresh (re-sync) every 15 minutes
- AC4: Skip copy if file has not changed (use etag or checksum comparison)

Commit plan rules:
- Each commit ≤ 250 lines
- Conventional Commits format
- Each commit leaves the codebase in a deployable state
- Tests written alongside each commit

Output format per commit:
  Commit [N]: <type>(<scope>): <description>
  Files: <list>
  What changes: <description>
  AC coverage: <AC-N>
  Tests: <what to test>
```

---

## PROMPT — PART 4: EXECUTE ONE COMMIT

```
Implement Commit [N] only.

After implementation:
1. Show a diff summary
2. Confirm which AC is now satisfied
3. List tests that should pass
4. STOP — wait for my review before proceeding to Commit [N+1]
```

---

## OpenShift Pre-Deploy Checklist

Before merging:
- [ ] PVC mounted in Deployment YAML at correct path
- [ ] PVC accessModes: ReadWriteMany (multi-pod) or ReadWriteOnce (single sync pod)
- [ ] S3 credentials in a Secret (not ConfigMap)
- [ ] Sync interval and PVC path in ConfigMap
- [ ] Readiness probe does NOT depend on sync completion
- [ ] Sync job is idempotent (restartable mid-sync without corruption)
- [ ] Resource requests/limits account for I/O during sync window
