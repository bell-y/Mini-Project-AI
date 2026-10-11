import unittest
from unittest.mock import patch, MagicMock
import requests
import os

from services.cleaner import (
    cleanse_text,
    TextCleansingError,
    get_api_key,
    AIFORTHAI_TEXT_CLEANSING_URL
)


class TestTextCleanerService(unittest.TestCase):

    def test_cleanse_text_empty_input(self):
        """Test that empty or whitespace-only text raises TextCleansingError."""
        with self.assertRaises(TextCleansingError) as ctx:
            cleanse_text("")
        self.assertEqual(ctx.exception.status_code, 400)

        with self.assertRaises(TextCleansingError) as ctx:
            cleanse_text("   \n\t  ")
        self.assertEqual(ctx.exception.status_code, 400)

    @patch.dict(os.environ, {"AIFORTHAI_API_KEY": ""}, clear=True)
    def test_get_api_key_missing(self):
        """Test that missing API key raises TextCleansingError."""
        with self.assertRaises(TextCleansingError) as ctx:
            get_api_key()
        self.assertEqual(ctx.exception.status_code, 400)
        self.assertIn("AIFORTHAI_API_KEY", ctx.exception.message)

    @patch.dict(os.environ, {"AIFORTHAI_API_KEY": "your_actual_api_key_here"})
    def test_get_api_key_placeholder(self):
        """Test that default placeholder API key raises TextCleansingError."""
        with self.assertRaises(TextCleansingError) as ctx:
            get_api_key()
        self.assertEqual(ctx.exception.status_code, 400)

    @patch("services.cleaner.requests.post")
    def test_cleanse_text_success(self, mock_post):
        """Test successful API response with original_text and cleansing_text."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "original_text": "วันนีอากาศดีมากกก",
            "cleansing_text": "วันนี้อากาศดีมาก"
        }
        mock_post.return_value = mock_response

        result = cleanse_text("วันนีอากาศดีมากกก", api_key="test_api_key_123")

        self.assertTrue(result["success"])
        self.assertEqual(result["original_text"], "วันนีอากาศดีมากกก")
        self.assertEqual(result["cleansing_text"], "วันนี้อากาศดีมาก")

        # Verify POST payload and headers
        mock_post.assert_called_once_with(
            AIFORTHAI_TEXT_CLEANSING_URL,
            data={"text": "วันนีอากาศดีมากกก"},
            headers={
                "Apikey": "test_api_key_123",
                "Content-Type": "application/x-www-form-urlencoded"
            },
            timeout=30
        )

    @patch("services.cleaner.requests.post")
    def test_cleanse_text_timeout(self, mock_post):
        """Test handling of requests.exceptions.Timeout."""
        mock_post.side_effect = requests.exceptions.Timeout()

        with self.assertRaises(TextCleansingError) as ctx:
            cleanse_text("ทดสอบ", api_key="test_key")
        self.assertEqual(ctx.exception.status_code, 504)
        self.assertIn("เวลานานเกินกำหนด", ctx.exception.message)

    @patch("services.cleaner.requests.post")
    def test_cleanse_text_connection_error(self, mock_post):
        """Test handling of connection error."""
        mock_post.side_effect = requests.exceptions.ConnectionError()

        with self.assertRaises(TextCleansingError) as ctx:
            cleanse_text("ทดสอบ", api_key="test_key")
        self.assertEqual(ctx.exception.status_code, 502)
        self.assertIn("ไม่สามารถเชื่อมต่อ", ctx.exception.message)

    @patch("services.cleaner.requests.post")
    def test_cleanse_text_unauthorized_401(self, mock_post):
        """Test handling of HTTP 401/403 Unauthorized."""
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.text = '{"message": "Unauthorized"}'
        mock_post.return_value = mock_response

        with self.assertRaises(TextCleansingError) as ctx:
            cleanse_text("ทดสอบ", api_key="invalid_key")
        self.assertEqual(ctx.exception.status_code, 401)
        self.assertIn("API Key", ctx.exception.message)

    @patch("services.cleaner.requests.post")
    def test_cleanse_text_rate_limit_429(self, mock_post):
        """Test handling of HTTP 429 Rate Limit."""
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_response.text = '{"message": "Rate limit exceeded"}'
        mock_post.return_value = mock_response

        with self.assertRaises(TextCleansingError) as ctx:
            cleanse_text("ทดสอบ", api_key="test_key")
        self.assertEqual(ctx.exception.status_code, 429)
        self.assertIn("Rate Limit", ctx.exception.message)

    @patch("services.cleaner.requests.post")
    def test_cleanse_text_server_error_500(self, mock_post):
        """Test handling of HTTP 500 Internal Server Error."""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_post.return_value = mock_response

        with self.assertRaises(TextCleansingError) as ctx:
            cleanse_text("ทดสอบ", api_key="test_key")
        self.assertEqual(ctx.exception.status_code, 502)
        self.assertIn("ขัดข้องชั่วคราว", ctx.exception.message)

    @patch("services.cleaner.requests.post")
    def test_cleanse_text_invalid_json(self, mock_post):
        """Test handling when response from server is not valid JSON."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_response.text = "<html><body>Error</body></html>"
        mock_post.return_value = mock_response

        with self.assertRaises(TextCleansingError) as ctx:
            cleanse_text("ทดสอบ", api_key="test_key")
        self.assertEqual(ctx.exception.status_code, 502)
        self.assertIn("ไม่อยู่ในรูปแบบ JSON", ctx.exception.message)

    @patch("services.cleaner.requests.post")
    def test_cleanse_text_missing_cleansing_text_key(self, mock_post):
        """Test handling when JSON is missing cleansing_text."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"error": "Invalid format"}
        mock_post.return_value = mock_response

        with self.assertRaises(TextCleansingError) as ctx:
            cleanse_text("ทดสอบ", api_key="test_key")
        self.assertEqual(ctx.exception.status_code, 502)
        self.assertIn("Invalid format", ctx.exception.message)


if __name__ == "__main__":
    unittest.main()
