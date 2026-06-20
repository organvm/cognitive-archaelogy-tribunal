import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cognitive_tribunal.modules.archive_scanner import ArchiveScanner

class TestArchiveScannerSecurity(unittest.TestCase):

    def setUp(self):
        self.scanner = ArchiveScanner()

    def test_scan_directory_unsafe_posix_root(self):
        """Test that scanning the root directory on POSIX returns an error."""
        with patch.object(ArchiveScanner, '_scan_recursive') as mock_scan:
            result = self.scanner.scan_directory('/')

            if 'error' not in result:
                 self.fail("Security check failed: scan_directory('/') did not return an error.")

            self.assertIn("Unsafe path", result['error'])
            mock_scan.assert_not_called()

    def test_scan_directory_unsafe_posix_etc(self):
        """Test that scanning /etc is blocked."""
        with patch.object(ArchiveScanner, '_scan_recursive') as mock_scan:
            result = self.scanner.scan_directory('/etc')

            if 'error' not in result:
                 self.fail("Security check failed: scan_directory('/etc') did not return an error.")

            self.assertIn("Unsafe path", result['error'])
            mock_scan.assert_not_called()

    @patch('os.name', 'nt')
    @patch('os.sep', '\\')
    def test_is_unsafe_path_windows(self):
        """Test Windows unsafe path detection logic directly."""
        if not hasattr(self.scanner, 'is_unsafe_path'):
            self.skipTest("is_unsafe_path not implemented yet")

        unsafe_paths = ['C:\\', 'C:\\Windows', 'C:\\Program Files']

        for p_str in unsafe_paths:
            # Create a mock for the path passed to is_unsafe_path
            mock_input_path = MagicMock(spec=Path)

            # Create a mock for the resolved path (abs_path)
            mock_abs_path = MagicMock(spec=Path)
            mock_abs_path.__str__.return_value = p_str

            # Configure resolve() to return our mocked abs_path
            mock_input_path.resolve.return_value = mock_abs_path

            # Configure anchor on abs_path
            if p_str == 'C:\\':
                mock_abs_path.anchor = 'C:\\'
            else:
                mock_abs_path.anchor = 'C:\\'

            self.assertTrue(self.scanner.is_unsafe_path(mock_input_path), f"Should block {p_str}")

    @patch('os.name', 'posix')
    def test_is_unsafe_path_posix(self):
        """Test POSIX unsafe path detection logic directly."""
        if not hasattr(self.scanner, 'is_unsafe_path'):
            self.skipTest("is_unsafe_path not implemented yet")

        unsafe_paths = ['/', '/etc', '/proc', '/sys']

        for p_str in unsafe_paths:
            # We can use real Paths for POSIX testing since we are on POSIX (usually)
            # But strictly speaking we should probably mock to be consistent/safe
            p = Path(p_str)
            self.assertTrue(self.scanner.is_unsafe_path(p), f"Should block {p_str}")

        safe_paths = ['/home/user/documents', '/tmp/safe']
        for p_str in safe_paths:
             p = Path(p_str)
             self.assertFalse(self.scanner.is_unsafe_path(p), f"Should allow {p_str}")

if __name__ == '__main__':
    unittest.main()
