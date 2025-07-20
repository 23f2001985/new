from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from PIL import Image
import pytesseract
import io
import re

# If you're on Windows and Tesseract is not in PATH, uncomment and set path:
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

app = FastAPI()

@app.post("/captcha")
async def solve_captcha(image: UploadFile = File(...)):
    try:
        # Step 1: Read image bytes
        image_bytes = await image.read()
        image = Image.open(io.BytesIO(image_bytes))

        # Step 2: OCR with pytesseract
        text = pytesseract.image_to_string(image)

        # Step 3: Extract two 8-digit numbers using regex
        # Remove spaces and find two 8-digit numbers with optional symbols between
        clean_text = text.replace(" ", "")
        match = re.findall(r"(\d{8})\D+(\d{8})", clean_text)

        if not match:
            return JSONResponse({"error": "Could not parse two 8-digit numbers."}, status_code=400)

        a, b = match[0]
        result = int(a) * int(b)

        # Step 4: Return result
        return {
            "answer": result,
            "email": "23f2001985@ds.study.iitm.ac.in"
        }

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
