import unittest
from unittest.mock import patch
import json

from app import app
from services.cleaner import TextCleansingError


class TestAppEndpoints(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config["TESTING"] = True

    def test_get_index(self):
        """Test that GET / returns 200 and loads HTML with Thai Text Cleaner."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Thai Text Cleaner", response.get_data(as_text=True))
        self.assertIn("แก้ไขข้อความ", response.get_data(as_text=True))

    def test_get_api_status(self):
        """Test GET /api/status returns online state."""
        response = self.client.get("/api/status")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "online")
        self.assertIn("api_key_configured", data)

    def test_clean_non_json_request(self):
        """Test POST /api/clean with non-JSON body returns 400."""
        response = self.client.post("/api/clean", data="text=hello")
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertFalse(data["success"])

    def test_clean_missing_text_field(self):
        """Test POST /api/clean missing 'text' field returns 400."""
        response = self.client.post(
            "/api/clean",
            data=json.dumps({}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertFalse(data["success"])
        self.assertIn("text", data["error"])

    def test_clean_empty_text(self):
        """Test POST /api/clean with empty text returns 400."""
        response = self.client.post(
            "/api/clean",
            data=json.dumps({"text": "   "}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertFalse(data["success"])
        self.assertIn("กรุณากรอกข้อความ", data["error"])

    @patch("app.cleanse_text")
    def test_clean_success(self, mock_cleanse):
        """Test POST /api/clean success with mocked cleaner."""
        mock_cleanse.return_value = {
            "success": True,
            "original_text": "วันนีอากาศดีมากกก",
            "cleansing_text": "วันนี้อากาศดีมาก",
            "raw_response": {}
        }

        response = self.client.post(
            "/api/clean",
            data=json.dumps({"text": "วันนีอากาศดีมากกก"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["success"])
        self.assertEqual(data["original_text"], "วันนีอากาศดีมากกก")
        self.assertEqual(data["cleansing_text"], "วันนี้อากาศดีมาก")

    @patch("app.cleanse_text")
    def test_clean_api_error_handling(self, mock_cleanse):
        """Test POST /api/clean properly relays TextCleansingError."""
        mock_cleanse.side_effect = TextCleansingError(
            message="API Key ของ AI for Thai ไม่ถูกต้อง",
            status_code=401,
            details={"http_status": 401}
        )

        response = self.client.post(
            "/api/clean",
            data=json.dumps({"text": "ทดสอบ"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertFalse(data["success"])
        self.assertIn("API Key", data["error"])
        self.assertEqual(data["details"]["http_status"], 401)


if __name__ == "__main__":
    unittest.main()
