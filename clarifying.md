# Clarifying Questions for Team Lead
## Ticket: PVC Embedding Sync / Knowledge Assistant Grounding Service

These questions should be answered BEFORE starting implementation to avoid rework.

---

### Storage & File Format

1. **What is the embedding file format?**
   - `.npy`, `.pkl`, `.faiss`, `.bin`, `.parquet`, or other?
   - Are all embedding files the same format or mixed?

2. **What is the expected size of the embedding dataset on S3?**
   - Total GB? Number of files? Average file size?
   - This drives PVC size request and sync duration estimates.

3. **What is the S3 bucket structure / prefix?**
   - Is there a single prefix (e.g. `embeddings/`) or multiple subdirectories?
   - Are there versioned paths (e.g. `embeddings/v1/`, `embeddings/v2/`)?

4. **Should ALL files under the prefix be synced, or only specific file types?**

---

### Change Detection

5. **What method should be used to detect "file has not changed"?**
   - S3 ETag comparison (default, fast)?
   - MD5/SHA256 checksum of file content?
   - Last-modified timestamp?
   - This affects implementation complexity and reliability.

6. **What happens if a file is DELETED from S3 — should it also be deleted from PVC?**
   - Or should PVC be append-only?

---

### Scheduling & Concurrency

7. **Is the 15-minute refresh a hard requirement or a starting default?**
   - Should it be configurable via env var / ConfigMap?

8. **How many replicas will this service run in OpenShift?**
   - If more than 1 replica, who owns the sync job?
   - Should there be a dedicated sync sidecar or init container, or does the main pod sync?
   - PVC access mode depends on this: `ReadWriteOnce` vs `ReadWriteMany`.

9. **Should the sync run at startup (before serving requests) or only on the timer?**
   - If at startup: readiness probe must wait for first sync to complete.
   - If timer-only: service starts with stale/empty PVC until first sync window.

---

### Embedding Loading

10. **Are embeddings loaded once at startup into memory, or read from disk per request?**
    - If in-memory: a reload mechanism is needed after each sync (hot reload vs restart).
    - If from disk: file locks or atomic file swap needed during sync.

11. **Is there a version-pinning requirement?**
    - Can the service mid-flight switch to a newly synced embedding set, or should it
      finish current requests with the old set before swapping?

---

### OpenShift / Infrastructure

12. **Is there an existing PVC already provisioned, or does one need to be created?**
    - If new: what StorageClass should be used? (e.g. `ocs-storagecluster-cephfs` for RWX)

13. **Are S3 credentials (access key / secret) already stored in an OpenShift Secret?**
    - Or will that need to be created as part of this ticket?

14. **Is there an existing ConfigMap for this service?**
    - Or should one be created for `PVC_MOUNT_PATH`, `SYNC_INTERVAL_SECONDS`, etc.?

15. **What namespace does this service live in?**

---

### Testing & Acceptance

16. **Is there a test S3 bucket or mock available for integration tests?**
    - LocalStack? MinIO? A dedicated dev bucket?

17. **How will AC4 ("do not copy if unchanged") be verified in the acceptance test?**
    - Is there a log line, metric, or endpoint that must show "X files skipped"?

18. **What is the definition of "done" for this ticket?**
    - Deployed to dev? Deployed to staging? Load tested?
    - Is there a qTest test case being written for this story?
