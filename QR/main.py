from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import qrcode
import io
import base64

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,                   # now valid
    allow_methods=["*"],
    allow_headers=["*"],
)


class QRRequest(BaseModel):
    text: str


@app.post("/generate_qr_code")
async def generate_qr_code(request: QRRequest):
    if not request.text.strip():
        return JSONResponse(content={"error": "Text cannot be empty"}, status_code=400)

    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(request.text)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")

    qr_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return {"qr_code": qr_base64}
