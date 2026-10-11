# 🇹🇭 Thai Text Cleaner (ระบบแก้ไขและทำความสะอาดข้อความภาษาไทย)

เว็บไซต์ทำความสะอาดและแก้ไขคำผิดภาษาไทย (Text Cleansing) โดยเชื่อมต่อกับ **AI for Thai API** (บริการ Text Cleansing) ออกแบบด้วย UI ภาษาไทยที่ทันสมัย สวยงาม เรียบง่าย ตอบโจทย์โปรเจกต์นักศึกษา พร้อมโครงสร้างโค้ดที่ปลอดภัย มีการแยก Backend และ Frontend ชัดเจน และมีระบบจัดการข้อผิดพลาดที่ครอบคลุม

---

## 🌟 คุณสมบัติเด่น (Features)

1. **ส่วนต่อประสานผู้ใช้ (UI) สวยงามทันสมัย**:
   - ออกแบบด้วยแบบอักษรภาษาไทย **Prompt** และ **Sarabun** อ่านง่าย สบายตา
   - รองรับการแสดงผลทั้งหน้าจอคอมพิวเตอร์และมือถือ (Responsive Web Design)
   - มีปุ่มข้อความตัวอย่าง 1-Click เพื่อการทดสอบและนำเสนอผลงานได้อย่างรวดเร็ว
2. **ระบบการทำงานหลัก**:
   - ช่องกรอกข้อความภาษาไทย พร้อมตัวนับจำนวนตัวอักษรแบบ Real-time
   - ปุ่ม **"แก้ไขข้อความ"** ที่เรียกใช้งาน Backend เพื่อเชื่อมต่อไปยัง AI for Thai
   - ปุ่มล้างข้อความและปุ่มคัดลอกผลลัพธ์ (Copy to Clipboard) พร้อมการแจ้งเตือน
3. **แสดงผลลัพธ์ชัดเจน**:
   - แสดงเปรียบเทียบระหว่าง **ข้อความต้นฉบับ (`original_text`)** และ **ข้อความที่แก้ไขแล้ว (`cleansing_text`)**
4. **ความปลอดภัยระดับมาตรฐาน**:
   - เก็บ API Key ไว้ในไฟล์ `.env` บนฝั่ง Backend เท่านั้น
   - ฝั่ง Frontend ไม่มีการเปิดเผย API Key ในโค้ดหรือใน Network Response
   - มีไฟล์ `.env.example` สำหรับเป็นแม่แบบ และเพิ่ม `.env` ใน `.gitignore` เรียบร้อยแล้ว
5. **การจัดการข้อผิดพลาดที่รัดกุม (Robust Error Handling)**:
   - แจ้งเตือนเมื่อยังไม่ได้ตั้งค่า API Key หรือ API Key ไม่ถูกต้อง (401/403)
   - จัดการกรณีข้อความว่างเปล่า ข้อความยาวเกิน หรือไม่ได้ส่งฟิลด์ตามที่กำหนด (400)
   - จัดการกรณีเครือข่ายขัดข้อง, Timeout (504), หรือเซิร์ฟเวอร์ปลายทางมีปัญหา (502)
   - ตรวจสอบความถูกต้องของรูปแบบ JSON ที่ตอบกลับมาจาก AI for Thai

---

## 📋 ข้อมูลทางเทคนิคของ API (AI for Thai)

- **บริการ**: Text Cleansing
- **Endpoint**: `https://api.aiforthai.in.th/textcleansing`
- **HTTP Method**: `POST`
- **Header**: `Apikey: <AIFORTHAI_API_KEY>`
- **Content-Type**: `application/x-www-form-urlencoded`
- **Parameter**: `text` (ข้อความภาษาไทยที่ต้องการแก้ไข)
- **Response JSON**:
  ```json
  {
    "original_text": "วันนีอากาศดีมากกก",
    "cleansing_text": "วันนี้อากาศดีมาก"
  }
  ```

---

## 📁 โครงสร้างโปรเจกต์ (Project Structure)

```text
thai-ai-project/
├── app.py                  # ไฟล์หลัก Flask Server (API Routes & UI Serving)
├── services/
│   ├── __init__.py
│   └── cleaner.py          # Service เรียก AI for Thai API พร้อม Error Handling
├── templates/
│   └── index.html          # หน้าเว็บ UI ภาษาไทย
├── static/
│   ├── css/
│   │   └── style.css       # สไตล์ CSS ที่ทันสมัยและรองรับ Responsive
│   └── js/
│       └── main.js         # JavaScript ฝั่งหน้าเว็บ จัดการ Form, Event, และ AJAX
├── tests/
│   ├── __init__.py
│   ├── test_cleaner.py     # Unit Tests สำหรับ Service และ API Error Cases
│   └── test_app.py         # Unit Tests สำหรับ Flask Routes
├── .env.example            # ไฟล์ตัวอย่างสำหรับการตั้งค่า Environment
├── .env                    # ไฟล์เก็บ API Key จริง (ไม่ถูก commit ขึ้น Git)
├── .gitignore              # ไฟล์กำหนดการละเว้นไฟล์ใน Git
├── requirements.txt        # รายการแพ็กเกจ Python ที่จำเป็น
└── README.md               # คู่มือการติดตั้งและใช้งานภาษาไทย
```

---

## 💻 ขั้นตอนการติดตั้งและรันบน Windows (Windows Guide)

### 1. ความต้องการของระบบ (Prerequisites)
- ระบบปฏิบัติการ Windows 10 หรือ Windows 11
- ติดตั้ง **Python 3.8** ขึ้นไป (แนะนำ Python 3.10 ขึ้นไป)
  - *ข้อแนะนำ*: ขณะติดตั้ง Python บน Windows ให้เลือกติ๊กถูก **"Add Python to PATH"**

ตรวจสอบการติดตั้ง Python โดยเปิด **PowerShell** หรือ **Command Prompt (cmd)** แล้วพิมพ์:
```powershell
python --version
```

---

### 2. เข้าสู่โฟลเดอร์โปรเจกต์
เปิด PowerShell หรือ Command Prompt แล้วนำทางมายังโฟลเดอร์โปรเจกต์:
```powershell
cd C:\Users\ASUS\thai-ai-project
```

---

### 3. (แนะนำ) สร้างและเปิดใช้งาน Virtual Environment
เพื่อป้องกันไม่ให้แพ็กเกจรบกวนกับระบบส่วนกลาง:
```powershell
# สร้าง venv
python -m venv venv

# เปิดใช้งาน venv บน PowerShell
.\venv\Scripts\Activate.ps1
```
> *หมายเหตุ*: หาก PowerShell ขึ้นข้อผิดพลาดเกี่ยวกับ Execution Policy ให้รันคำสั่ง:  
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` แล้วลอง Activate อีกครั้ง  
> หรือหากใช้ **Command Prompt (cmd)** ให้รัน:  
> `venv\Scripts\activate.bat`

---

### 4. ติดตั้ง Dependencies
ติดตั้งแพ็กเกจที่ระบุไว้ใน `requirements.txt`:
```powershell
pip install -r requirements.txt
```

---

### 5. การตั้งค่า API Key ในไฟล์ `.env`

1. สมัครสมาชิกและขอรับ API Key ฟรีได้ที่เว็บไซต์ [AI for Thai](https://aiforthai.in.th/)
2. หากยังไม่มีไฟล์ `.env` ให้คัดลอกจาก `.env.example`:
   ```powershell
   copy .env.example .env
   ```
3. เปิดไฟล์ `.env` ด้วย Notepad หรือ Visual Studio Code:
   ```powershell
   notepad .env
   ```
4. แก้ไขค่า `AIFORTHAI_API_KEY` ให้เป็นคีย์จริงที่คุณได้รับ เช่น:
   ```env
   AIFORTHAI_API_KEY=YOUR_ACTUAL_API_KEY_HERE
   HOST=127.0.0.1
   PORT=5000
   ```
5. บันทึกและปิดไฟล์

---

### 6. เริ่มต้นรันเว็บไซต์ (Start Server)

พิมพ์คำสั่งเพื่อรัน Backend Server:
```powershell
python app.py
```

เมื่อเซิร์ฟเวอร์เริ่มทำงาน จะปรากฏข้อความบนหน้าจอ:
```text
============================================================
  Thai Text Cleaner - AI for Thai Web Application
  URL: http://127.0.0.1:5000
============================================================
 * Serving Flask app 'app'
 * Running on http://127.0.0.1:5000
```

---

### 7. เข้าใช้งานเว็บไซต์ผ่าน Web Browser
เปิดเบราว์เซอร์ (Google Chrome, Microsoft Edge, Firefox) แล้วไปที่:
👉 **http://127.0.0.1:5000** หรือ **http://localhost:5000**

- ทดลองคลิกเลือก **"ข้อความตัวอย่าง"** หรือพิมพ์ข้อความภาษาไทยที่มีคำผิด
- กดปุ่ม **"แก้ไขข้อความ"**
- สังเกตสถานะการประมวลผล และผลลัพธ์ที่แสดงผลทั้ง **ข้อความต้นฉบับ** และ **ข้อความที่แก้ไขแล้ว**

---

## 🧪 การทดสอบระบบ (Testing)

โปรเจกต์นี้มีชุดทดสอบอัตโนมัติ (Automated Unit Tests) ครอบคลุมทั้งฝั่ง Service Logic และ API Endpoints รวมถึงจำลองสถานการณ์ Error ต่างๆ เช่น API Key หาย, Timeout, Invalid JSON, HTTP 401, HTTP 429, HTTP 500

รันคำสั่งทดสอบด้วยคำสั่ง:
```powershell
python -m unittest discover tests
```

ผลการทดสอบ:
```text
Ran 18 tests in 0.210s
OK
```

---

## 🛡️ การจัดการข้อผิดพลาด (Error Handling)

| กรณีที่เกิดขึ้น | สถานะ HTTP | การแสดงผลในระบบ |
| :--- | :--- | :--- |
| ยังไม่ได้ตั้งค่า API Key ใน `.env` | `400 Bad Request` | แจ้งเตือนสีส้มด้านบน และแสดงข้อความแนะนำให้กรอก API Key ใน `.env` |
| กรอกข้อความว่างเปล่า | `400 Bad Request` | แจ้งเตือน "กรุณากรอกข้อความภาษาไทยก่อนกดปุ่มแก้ไข" |
| API Key ไม่ถูกต้อง / สิทธิ์ไม่เพียงพอ | `401 Unauthorized` | แจ้งเตือน "API Key ของ AI for Thai ไม่ถูกต้อง หรือไม่มีสิทธิ์เข้าถึงบริการนี้" |
| เกินโควตาการใช้งาน | `429 Too Many Requests` | แจ้งเตือน "เรียกใช้งาน API เกินโควตาที่กำหนด กรุณารอสักครู่แล้วลองใหม่" |
| การเชื่อมต่ออินเทอร์เน็ตล้มเหลว | `502 Bad Gateway` | แจ้งเตือน "ไม่สามารถเชื่อมต่อกับบริการ AI for Thai ได้ กรุณาตรวจสอบอินเทอร์เน็ต" |
| เชื่อมต่อนานเกิน 30 วินาที | `504 Gateway Timeout` | แจ้งเตือน "การเชื่อมต่อกับ AI for Thai ใช้เวลานานเกินกำหนด" |
| AI for Thai ตอบกลับมาไม่ใช่ JSON | `502 Bad Gateway` | แจ้งเตือน "ข้อมูลที่ได้รับจาก AI for Thai ไม่อยู่ในรูปแบบ JSON ที่ถูกต้อง" |

---

## 👥 ข้อมูลเพิ่มเติมสำหรับโปรเจกต์นักศึกษา
- โค้ดถูกเขียนขึ้นตามหลัก Modular Architecture สะอาด เข้าใจง่าย เหมาะแก่การนำไปต่อยอด
- ปฏิบัติตามข้อกำหนดความปลอดภัย ไม่ฮาร์ดโค้ด Credential ในโค้ด
- รองรับการนำไปใช้ทำโครงงานวิชา Natural Language Processing (NLP), Web Development หรือ Artificial Intelligence Application
