import unittest
from unittest.mock import patch, MagicMock
from app import app, get_access_token, get_all_activities, get_latest_5_activity, get_latest_5_activity_by_sport

class StravaAPITestCase(unittest.TestCase):

    def setUp(self):
        """Set up test client for Flask."""
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.requests.post')
    def test_get_access_token_success(self, mock_post):
        """Test successful access token retrieval."""
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"access_token": "mock_token"}
        
        token = get_access_token()
        self.assertEqual(token, "mock_token")

    @patch('app.requests.post')
    def test_get_access_token_failure(self, mock_post):
        """Test access token failure."""
        mock_post.return_value.status_code = 400
        mock_post.return_value.json.return_value = {}

        token = get_access_token()
        self.assertIsNone(token)

    @patch('app.get_access_token', return_value="mock_token")
    @patch('app.requests.get')
    def test_get_all_activities_success(self, mock_get, mock_token):
        """Test fetching activities successfully."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{"id": 1, "sport_type": "run"}, {"id": 2, "sport_type": "bike"}]

        activities = get_all_activities()
        self.assertIsInstance(activities, list)
        self.assertEqual(len(activities), 2)

    @patch('app.get_access_token', return_value=None)
    def test_get_all_activities_failure(self, mock_token):
        """Test failure to fetch activities due to authentication failure."""
        activities = get_all_activities()
        self.assertIn("error", activities)
        self.assertEqual(activities["error"], "Failed to authenticate with Strava")

    @patch('app.get_all_activities', return_value=[{"id": 1, "sport_type": "run"}, {"id": 2, "sport_type": "bike"}])
    def test_get_latest_5_activity_success(self, mock_activities):
        """Test fetching latest 5 activities."""
        latest_activities = get_latest_5_activity()
        self.assertIsInstance(latest_activities, list)
        self.assertLessEqual(len(latest_activities), 5)

    @patch('app.get_all_activities', return_value=[])
    def test_get_latest_5_activity_no_activities(self, mock_activities):
        """Test no activities found case."""
        latest_activities = get_latest_5_activity()
        self.assertIn("error", latest_activities)
        self.assertEqual(latest_activities["error"], "No activities found")

    @patch('app.get_all_activities', return_value=[{"id": 1, "sport_type": "Run"}, {"id": 2, "sport_type": "Bike"}])
    def test_get_latest_5_activity_by_sport_success(self, mock_activities):
        """Test filtering activities by sport."""
        filtered_activities = get_latest_5_activity_by_sport("run")
        self.assertIsInstance(filtered_activities, list)
        self.assertEqual(len(filtered_activities), 1)

    @patch('app.get_all_activities', return_value=[{"id": 1, "sport_type": "Run"}])
    def test_get_latest_5_activity_by_sport_no_match(self, mock_activities):
        """Test no activities found for a given sport."""
        filtered_activities = get_latest_5_activity_by_sport("bike")
        self.assertIn("error", filtered_activities)
        self.assertEqual(filtered_activities["error"], "No activities found for this sport.")

    def test_routes(self):
        """Test API routes."""
        response = self.app.get('/latest')
        self.assertEqual(response.status_code, 200)

        response = self.app.get('/all')
        self.assertEqual(response.status_code, 200)

        response = self.app.get('/latest/run')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
