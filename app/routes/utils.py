from fastapi import APIRouter
import os

router = APIRouter()

@router.get("/api/info")
def get_info():
    base_url = os.getenv("BASE_URL", "http://localhost:8000")
    github_redirect = os.getenv("GITHUB_REDIRECT_URL", "https://usuarioap03-hash.github.io/hosting/")
    return {
        "base_url": base_url,
        "github_redirect": github_redirect
    }