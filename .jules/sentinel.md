## 2025-01-20 - Prevent System Directory Scanning
**Vulnerability:**
The `ArchiveScanner` module allowed users to scan any directory, including the filesystem root (`/` or `C:\`) and critical system directories (e.g., `/etc`, `C:\Windows`). This could lead to resource exhaustion (scanning millions of system files) or potential information disclosure if the report is shared.

**Learning:**
Relying solely on user input for directory paths in a scanner tool is risky. Even in a CLI tool, users might accidentally point to root. Using `pathlib.Path.resolve()` is crucial to handle symlinks and relative paths, but explicit checks against `path.anchor` (to detect root) and a blocklist of known system roots are necessary for safety.

**Prevention:**
Implemented an `is_unsafe_path` check in `ArchiveScanner` that:
1.  Compares `path.anchor` with the path to detect if the user is scanning the entire drive.
2.  Checks the path against a predefined list of platform-specific system directories (`UNSAFE_PATHS_POSIX` and `UNSAFE_PATHS_NT`).
3.  Returns an error immediately if an unsafe path is detected, preventing the recursive scan.
