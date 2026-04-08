from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from utils.auth import verify_token

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/user-status")
def user_status(authorization: str = Header(...), db: Session = Depends(get_db)):
    user_data = verify_token(authorization)

    user = db.query(User).filter(User.id == user_data["user_id"]).first()

    if not user:
        user = User(
            id=user_data["user_id"],
            email=user_data["email"],
            name=user_data["name"],
            wipes_remaining=3
        )
        db.add(user)
        db.commit()

    return {
        "name": user.name,
        "wipes_remaining": user.wipes_remaining
    }


@router.post("/consume-wipe")
def consume_wipe(authorization: str = Header(...), db: Session = Depends(get_db)):
    user_data = verify_token(authorization)

    user = db.query(User).filter(User.id == user_data["user_id"]).first()

    if user.wipes_remaining <= 0:
        return {"success": False, "message": "No wipes left"}

    user.wipes_remaining -= 1
    db.commit()

    return {
        "success": True,
        "remaining": user.wipes_remaining
    }