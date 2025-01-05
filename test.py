import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from collections import defaultdict
from main import find_git_repositories, get_commit_dates, prepare_heatmap_data

class TestContributionTool(unittest.TestCase):
    @patch("os.walk")
    def test_find_git_repositories(self, mock_walk):
        mock_walk.return_value = [
            ("/root", ["ccwc", "docs"], []),
            ("/root/ccwc", [".git"], []),
            ("/root/docs", [], []),
        ]
        result = find_git_repositories("/root")
        self.assertEqual(result, ["/root/ccwc"])

    @patch("main.Repo")
    def test_get_commit_dates(self, mock_repo):
        mock_repo.return_value = MagicMock(
            iter_commits=MagicMock(
                return_value=[
                    MagicMock(committed_date=(datetime.now() - timedelta(days=1)).timestamp()),
                    MagicMock(committed_date=(datetime.now() - timedelta(days=5)).timestamp()),
                ]
            )
        )
        result = get_commit_dates("/path/to/repo", 7)
        expected_dates = [
            (datetime.now() - timedelta(days=1)).date(),
            (datetime.now() - timedelta(days=5)).date(),
        ]
        self.assertEqual(result, expected_dates)

    def test_prepare_heatmap_data(self):
        dates = [
            datetime.now().date() - timedelta(days=1),
            datetime.now().date() - timedelta(days=1),
            datetime.now().date() - timedelta(days=5),
        ]
        days = 7
        date_range, heatmap_data = prepare_heatmap_data(dates, days)

        start_date = datetime.now().date() - timedelta(days=days)
        expected_date_range = [start_date + timedelta(days=i) for i in range(days + 1)]
        expected_heatmap_data = [0] * (days + 1)
        expected_heatmap_data[-2] = 2  # 2 commits 1 day ago
        expected_heatmap_data[-6] = 1  # 1 commit 5 days ago

        self.assertEqual(date_range, expected_date_range)
        self.assertEqual(heatmap_data, expected_heatmap_data)

if __name__ == "__main__":
    unittest.main()
