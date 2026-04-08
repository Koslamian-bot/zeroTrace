from fastapi import HTTPException

def verify_token(token: str):
    # For now mock
    if not token:
        raise HTTPException(status_code=401, detail="Invalid token")

    return {
        "user_id": "demo-user",
        "email": "demo@gmail.com",
        "name": "Rowin"
    }