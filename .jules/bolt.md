## 2024-05-23 - Hashing Performance Optimization
**Learning:** `xxhash` provides a massive performance boost over `sha256` for file hashing, especially for larger files (8-10x faster).
**Action:** Default to `xxhash` for non-cryptographic use cases like file deduplication. Always buffer I/O operations (64KB is a good balance).
