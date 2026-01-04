import os
import uuid
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from tts import text_to_mp3
from video import mp3_to_mp4
from fastapi import Depends, Header

API_KEY = "my_secret_key_123"

def verify_api_key(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")


# -------------------- PATH SETUP (IMPORTANT) --------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
ASSET_IMAGE = os.path.join(BASE_DIR, "assets", "bg.jpg")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# -------------------- FASTAPI APP --------------------

app = FastAPI()

# -------------------- GENERATE API --------------------

@app.post("/generate", dependencies=[Depends(verify_api_key)])
def generate(text: str, format: str = "mp4"):
    if len(text) > 4000:
        raise HTTPException(status_code=400, detail="Text too long")

    file_id = str(uuid.uuid4())

    # MP3 path
    mp3_path = os.path.join(OUTPUT_DIR, f"{file_id}.mp3")
    text_to_mp3(text, mp3_path)

    # MP4 generation
    if format == "mp4":
        mp4_path = os.path.join(OUTPUT_DIR, f"{file_id}.mp4")
        mp3_to_mp4(mp3_path, mp4_path, ASSET_IMAGE)

        return {
            "file": f"{file_id}.mp4",
            "url": f"/download/{file_id}.mp4"
        }

    # Fallback MP3
    return {
        "file": f"{file_id}.mp3",
        "url": f"/download/{file_id}.mp3"
    }

# -------------------- DOWNLOAD API --------------------

@app.get("/download/{filename}")
def download(filename: str):
    file_path = os.path.join(OUTPUT_DIR, filename)
    print("Trying to download:", file_path)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    media_type = "video/mp4" if filename.endswith(".mp4") else "audio/mpeg"

    return FileResponse(
        file_path,
        media_type=media_type,
        filename=filename
    )

