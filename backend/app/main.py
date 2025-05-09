from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.middlewares.auth import auth_middleware
from app.routes import auth, product, recipe, upload
from pathlib import Path

from app.utils.upload import create_upload_directories

app = FastAPI()

# upload
create_upload_directories()

# cors
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# middlewares
app.middleware("http")(auth_middleware)

# routes
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(product.router, prefix="/product", tags=["product"])
app.include_router(recipe.router, prefix="/recipe", tags=["recipe"])
app.include_router(upload.router, prefix="/upload", tags=["upload"])