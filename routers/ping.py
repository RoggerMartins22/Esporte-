from fastapi import APIRouter

router = APIRouter(
    prefix="/ping",
    tags=["ping"],
)

@router.api_route("/", methods=["GET", "HEAD"])
async def ping():
    return {"message": "pong"}