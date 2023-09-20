from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health():
    """Health endpoint."""
    return {"status": "It works ✨!"}
