import os
import requests
from typing import Dict, Any, Tuple

AIFORTHAI_TEXT_CLEANSING_URL = "https://api.aiforthai.in.th/textcleansing"
PLACEHOLDER_KEYS = {
    "",
    "your_actual_api_key_here",
    "YOUR_AIFORTHAI_API_KEY_HERE",
    "YOUR_API_KEY",
}


class TextCleansingError(Exception):
    """Custom exception for text cleansing API errors."""

    def __init__(self, message: str, status_code: int = 500, details: Any = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details


def get_api_key() -> str:
    """Retrieve and validate the AI for Thai API Key from environment."""
    api_key = os.getenv("AIFORTHAI_API_KEY", "").strip()
    if not api_key or api_key in PLACEHOLDER_KEYS:
        raise TextCleansingError(
            message="ยังไม่ได้ตั้งค่า AIFORTHAI_API_KEY ในไฟล์ .env หรือยังเป็นค่าเริ่มต้น กรุณาระบุ API Key ที่ถูกต้อง",
            status_code=400,
            details={"config_hint": "กรุณาเปิดไฟล์ .env และแทนที่ค่า AIFORTHAI_API_KEY ด้วยคีย์จริงจาก https://aiforthai.in.th/"}
        )
    return api_key


def cleanse_text(text: str, api_key: str = None, timeout: int = 30) -> Dict[str, Any]:
    """
    Call AI for Thai Text Cleansing API.
    
    API Specs:
    - Endpoint: https://api.aiforthai.in.th/textcleansing
    - Method: POST
    - Header: Apikey
    - Content-Type: application/x-www-form-urlencoded
    - Parameter: text
    - Response JSON: original_text, cleansing_text
    """
    if text is None or not str(text).strip():
        raise TextCleansingError(
            message="กรุณากรอกข้อความภาษาไทยที่ต้องการแก้ไข",
            status_code=400
        )

    clean_input = str(text).strip()
    key = api_key or get_api_key()

    url = AIFORTHAI_TEXT_CLEANSING_URL
    headers = {
        "Apikey": key,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "text": clean_input
    }

    try:
        response = requests.post(url, data=data, headers=headers, timeout=timeout)
    except requests.exceptions.Timeout:
        raise TextCleansingError(
            message=f"การเชื่อมต่อกับ AI for Thai ใช้เวลานานเกินกำหนด ({timeout} วินาที) กรุณาลองใหม่อีกครั้ง",
            status_code=504
        )
    except requests.exceptions.ConnectionError:
        raise TextCleansingError(
            message="ไม่สามารถเชื่อมต่อกับบริการ AI for Thai ได้ กรุณาตรวจสอบการเชื่อมต่ออินเทอร์เน็ต",
            status_code=502
        )
    except requests.exceptions.RequestException as e:
        raise TextCleansingError(
            message=f"เกิดข้อผิดพลาดในการส่งคำขอไปยัง AI for Thai: {str(e)}",
            status_code=500
        )

    # Handle HTTP status codes
    if response.status_code == 401 or response.status_code == 403:
        raise TextCleansingError(
            message="API Key ของ AI for Thai ไม่ถูกต้อง หรือไม่มีสิทธิ์เข้าถึงบริการนี้ (HTTP 401/403)",
            status_code=401,
            details={"http_status": response.status_code, "raw_response": response.text[:200]}
        )
    elif response.status_code == 429:
        raise TextCleansingError(
            message="เรียกใช้งาน API เกินโควตาที่กำหนด (Rate Limit Exceeded) กรุณารอสักครู่แล้วลองใหม่",
            status_code=429,
            details={"http_status": response.status_code}
        )
    elif response.status_code >= 500:
        raise TextCleansingError(
            message=f"บริการของ AI for Thai ขัดข้องชั่วคราว (HTTP {response.status_code}) กรุณาลองใหม่ในภายหลัง",
            status_code=502,
            details={"http_status": response.status_code, "raw_response": response.text[:200]}
        )
    elif response.status_code != 200:
        raise TextCleansingError(
            message=f"เกิดข้อผิดพลาดจากบริการ AI for Thai (HTTP {response.status_code})",
            status_code=response.status_code,
            details={"http_status": response.status_code, "raw_response": response.text[:200]}
        )

    # Parse and validate JSON response
    try:
        result = response.json()
    except Exception:
        raise TextCleansingError(
            message="ข้อมูลที่ได้รับจาก AI for Thai ไม่อยู่ในรูปแบบ JSON ที่ถูกต้อง",
            status_code=502,
            details={"raw_response": response.text[:300]}
        )

    if not isinstance(result, dict):
        raise TextCleansingError(
            message=f"รูปแบบข้อมูลที่ได้รับจาก AI for Thai ไม่ถูกต้อง (คาดหวัง Object แต่ได้ {type(result).__name__})",
            status_code=502,
            details={"result": result}
        )

    # Check for expected keys: original_text, cleansing_text
    # Some APIs might wrap or return errors inside JSON
    if "cleansing_text" not in result:
        # Check if an error message is returned in JSON
        error_msg = result.get("message") or result.get("error") or result.get("msg")
        if error_msg:
            raise TextCleansingError(
                message=f"AI for Thai แจ้งข้อผิดพลาด: {error_msg}",
                status_code=502,
                details={"result": result}
            )
        raise TextCleansingError(
            message="ไม่พบข้อมูลผลลัพธ์ cleansing_text จาก AI for Thai",
            status_code=502,
            details={"result": result}
        )

    original_text = result.get("original_text", clean_input)
    cleansing_text = result.get("cleansing_text", "")

    return {
        "success": True,
        "original_text": original_text,
        "cleansing_text": cleansing_text,
        "raw_response": result
    }
