from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services.quadras import create_quadrant_service
from schemas.quadras import QuadraCreate
from auth.auth import token_verifier
from database.database import get_db

router = APIRouter(
    prefix="/quadras",
    tags=["quadras"],
    dependencies=[Depends(token_verifier)]
)

@router.post("/cadastrar")
async def register_quadrant(quadra: QuadraCreate, db: Session = Depends(get_db)):
    return create_quadrant_service(db=db, quadra=quadra)