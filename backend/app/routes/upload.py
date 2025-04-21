from enum import Enum
from uuid import uuid4
from mimetypes import guess_type

from fastapi import APIRouter, HTTPException, UploadFile
from starlette.responses import JSONResponse, FileResponse

from app.utils.upload import ALLOWED_MIME_TYPES, MAX_FILE_SIZE, UPLOAD_DIR

router = APIRouter()

class TypeName(str, Enum):
    thumbnail = "thumbnail"

@router.post("/{type}")
async def upload_image(type: TypeName, file: UploadFile | None = None):
    if not file:
        raise HTTPException(status_code=400, detail="No upload file sent")

    # check mime type
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=400, detail=f"Unsupported content type {file.content_type}")

    # check size
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="Too big file (10MB limit)")

    # generate unique name
    filename = f"{uuid4().hex}_{file.filename}"
    filename = (filename
        .replace(" ", "-")
        .replace("(", "-")
        .replace(")", "-")
    )
    filepath = UPLOAD_DIR / type / filename

    # write file
    with filepath.open("wb") as buffer:
        buffer.write(content)

    return JSONResponse(status_code=201, content={
        "type": type,
        "filename": filename,
    })

@router.get("/{type}/{filename}")
async def get_image(type: TypeName, filename: str):
    filepath = UPLOAD_DIR / type / filename

    if not filepath.exists():
        raise HTTPException(status_code=404, detail=f"File {filename} not found")

    # detect mimetype
    mime_type, _ = guess_type(str(filepath))

    return FileResponse(path=filepath, media_type=mime_type or "image/jpeg")