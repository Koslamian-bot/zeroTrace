from fastapi import FastAPI
from routes import wipes, certificates
from database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(wipes.router)
app.include_router(certificates.router)

@app.get("/")
def root():
    return {"message": "ZeroTrace Backend Running"}