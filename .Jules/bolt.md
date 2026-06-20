## 2024-05-24 - Python 3.11+ hashlib.file_digest
**Learning:** `hashlib.file_digest()` is a significant optimization over manual chunk reading (approx 1.1x faster). It moves the file reading loop from Python to C, releasing the GIL.
**Action:** Always check for `hashlib.file_digest` availability when performing file hashing operations in Python, while maintaining a fallback for older versions.
