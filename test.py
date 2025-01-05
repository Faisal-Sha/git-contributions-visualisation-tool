import unittest
from unittest.mock import MagicMock, patch
from your_script_name import get_repo_stats

class TestGitStats(unittest.TestCase):
    @patch("your_script_name.Repo")
    def test_get_repo_stats(self, MockRepo):
        mock_repo = MagicMock()
        mock_commit = MagicMock()
        mock_commit.author.email = "user@example.com"

        mock_repo.iter_commits.return_value = [mock_commit] * 5
        MockRepo.return_value = mock_repo

        stats = get_repo_stats("/fake/path", 30)
        self.assertEqual(stats["total_commits"], 5)
        self.assertEqual(stats["contributors"]["user@example.com"], 5)

    @patch("your_script_name.Repo")
    def test_bare_repo(self, MockRepo):
        mock_repo = MagicMock()
        mock_repo.bare = True
        MockRepo.return_value = mock_repo

        stats = get_repo_stats("/bare/repo", 30)
        self.assertEqual(stats["total_commits"], 0)
        self.assertEqual(len(stats["contributors"]), 0)

if __name__ == "__main__":
    unittest.main()
