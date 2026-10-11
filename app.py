import os
import sys
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify

# Load environment variables from .env file
load_dotenv()

from services.cleaner import cleanse_text, TextCleansingError, PLACEHOLDER_KEYS

app = Flask(__name__)


@app.route("/")
def index():
    """Render the Thai Text Cleaner web UI."""
    return render_template("index.html")


@app.route("/api/status", methods=["GET"])
def api_status():
    """
    Check server and configuration status.
    Returns whether the AIFORTHAI_API_KEY has been configured (without exposing the key).
    """
    api_key = os.getenv("AIFORTHAI_API_KEY", "").strip()
    is_configured = bool(api_key and api_key not in PLACEHOLDER_KEYS)
    return jsonify({
        "status": "online",
        "api_key_configured": is_configured,
        "service": "AI for Thai - Text Cleansing"
    })


@app.route("/api/clean", methods=["POST"])
def api_clean():
    """
    Endpoint for text cleansing.
    Accepts JSON payload: {"text": "..."}
    Calls AI for Thai Text Cleansing API via backend.
    """
    if not request.is_json:
        return jsonify({
            "success": False,
            "error": "รูปแบบคำขอไม่ถูกต้อง กรุณาส่งข้อมูลแบบ JSON (Content-Type: application/json)"
        }), 400

    data = request.get_json() or {}
    text = data.get("text")

    if text is None:
        return jsonify({
            "success": False,
            "error": "กรุณาระบุฟิลด์ 'text' ในคำขอ"
        }), 400

    if not isinstance(text, str):
        return jsonify({
            "success": False,
            "error": "ข้อความต้องเป็นสตริง (String)"
        }), 400

    if not text.strip():
        return jsonify({
            "success": False,
            "error": "กรุณากรอกข้อความภาษาไทยที่ต้องการแก้ไข"
        }), 400

    # Limit text length to prevent misuse or massive payload issues
    if len(text) > 10000:
        return jsonify({
            "success": False,
            "error": "ข้อความมีความยาวเกินกำหนด (สูงสุด 10,000 ตัวอักษร)"
        }), 400

    try:
        result = cleanse_text(text)
        return jsonify(result), 200
    except TextCleansingError as e:
        response_payload = {
            "success": False,
            "error": e.message
        }
        if e.details:
            response_payload["details"] = e.details
        return jsonify(response_payload), e.status_code
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"เกิดข้อผิดพลาดที่ไม่คาดคิดภายในเซิร์ฟเวอร์: {str(e)}"
        }), 500


if __name__ == "__main__":
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "5000"))
    debug_mode = os.getenv("FLASK_DEBUG", "false").lower() in ("true", "1")
    
    print("=" * 60)
    print("  Thai Text Cleaner - AI for Thai Web Application")
    print(f"  URL: http://{host}:{port}")
    print("=" * 60)
    
    app.run(host=host, port=port, debug=debug_mode)
