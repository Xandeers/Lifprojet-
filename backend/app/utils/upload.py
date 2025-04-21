from pathlib import Path

ALLOWED_MIME_TYPES = {"image/jpeg", "image/jpg", "image/png", "image/webp"}
MAX_FILE_SIZE = 1024 * 1024 * 10
UPLOAD_DIR = Path(__file__).parent.parent.parent / "upload"
UPLOAD_SUBDIR = ["thumbnail"]

def create_upload_directories():
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    for d in UPLOAD_SUBDIR:
        (UPLOAD_DIR / d).mkdir(exist_ok=True)