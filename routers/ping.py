from fastapi import APIRouter

router = APIRouter(
    prefix="/ping",
    tags=["users"],
)

@router.api_route("/ping", methods=["GET", "HEAD"])
async def ping():
    return {"message": "pong"}