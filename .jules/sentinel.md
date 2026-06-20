## 2024-03-24 - [Path Traversal Protection]
**Vulnerability:** The `ArchiveScanner` lacked explicit checks for unsafe paths, allowing potential scanning of sensitive system directories (like `/etc`, `C:\Windows`) or the filesystem root. While `pathlib.Path.resolve()` handles `..` traversal, it doesn't prevent legitimate requests to scan critical paths.
**Learning:** Always explicitly block known unsafe paths (allow-list or deny-list) in file scanning utilities, even if path resolution is used. `Path.anchor` is a reliable way to check for root directory scans.
**Prevention:** Implemented `is_unsafe_path` with platform-specific deny-lists (`UNSAFE_PATHS_POSIX`, `UNSAFE_PATHS_NT`) and integrated it into `scan_directory` to block such requests before any file operations occur.
