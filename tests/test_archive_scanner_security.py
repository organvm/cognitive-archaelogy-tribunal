"""
Security tests for Archive Scanner module.
Verifies that unsafe paths are blocked.
"""

from cognitive_tribunal.modules.archive_scanner import ArchiveScanner
import unittest
from unittest.mock import MagicMock, patch
import os
import sys

# Add project root to path to ensure imports work
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

# pylint: disable=wrong-import-position


class TestArchiveScannerSecurity(unittest.TestCase):
    """Test suite for Archive Scanner security features."""

    @patch('cognitive_tribunal.modules.archive_scanner.Path')
    @patch.object(ArchiveScanner, '_scan_recursive')
    def test_unsafe_path_blocked_posix(self, mock_scan, mock_path_cls):
        """
        Test that scanning an unsafe path (like root) returns an error
        on POSIX.
        """
        # Setup mock to simulate filesystem root
        mock_root = MagicMock()
        mock_root.exists.return_value = True
        mock_root.is_dir.return_value = True
        mock_root.resolve.return_value = mock_root

        # Simulate path being '/'
        mock_root.__str__.return_value = '/'
        mock_root.anchor = '/'

        mock_path_cls.return_value = mock_root

        scanner = ArchiveScanner()

        # Action
        result = scanner.scan_directory('/')

        # Assertion
        self.assertIn('error', result, "Scanning root should return an error")
        self.assertTrue('unsafe' in result.get('error', '').lower(),
                        f"Error message should mention unsafe path, got: {result.get('error')}")

        mock_scan.assert_not_called()

    @patch('cognitive_tribunal.modules.archive_scanner.Path')
    @patch.object(ArchiveScanner, '_scan_recursive')
    @patch('os.name', 'nt')
    @patch('os.sep', '\\')
    def test_unsafe_path_blocked_windows(self, mock_scan, mock_path_cls):
        r"""
        Test that scanning an unsafe path (like C:\Windows) returns an error
        on Windows.
        """
        # Setup mock to simulate C:\Windows
        mock_root = MagicMock()
        mock_root.exists.return_value = True
        mock_root.is_dir.return_value = True
        mock_root.resolve.return_value = mock_root

        # Simulate path being 'C:\Windows'
        mock_root.__str__.return_value = 'C:\\Windows'
        mock_root.anchor = 'C:\\'

        mock_path_cls.return_value = mock_root

        scanner = ArchiveScanner()

        # Action
        result = scanner.scan_directory('C:\\Windows')

        # Assertion
        self.assertIn('error', result,
                      "Scanning system dir should return an error")
        self.assertTrue('unsafe' in result.get('error', '').lower(),
                        f"Error message should mention unsafe path, got: {result.get('error')}")

        mock_scan.assert_not_called()

    @patch('cognitive_tribunal.modules.archive_scanner.Path')
    @patch.object(ArchiveScanner, '_scan_recursive')
    def test_safe_path_allowed(self, mock_scan, mock_path_cls):
        """
        Test that scanning a safe path proceeds.
        """
        # Setup mock to simulate /home/user/docs
        mock_root = MagicMock()
        mock_root.exists.return_value = True
        mock_root.is_dir.return_value = True
        mock_root.resolve.return_value = mock_root

        mock_root.__str__.return_value = '/home/user/docs'
        mock_root.anchor = '/'

        mock_path_cls.return_value = mock_root

        scanner = ArchiveScanner()

        # Action
        scanner.scan_directory('/home/user/docs')

        # Assertion
        mock_scan.assert_called_once()


if __name__ == '__main__':
    unittest.main()
