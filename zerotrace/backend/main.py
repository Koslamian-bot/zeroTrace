from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import wipes, certificates, auth
from database import Base, engine

# Create tables in DB
Base.metadata.create_all(bind=engine)

app = FastAPI(title="ZeroTrace API", version="1.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(wipes.router, prefix="/wipes", tags=["wipes"])
app.include_router(certificates.router, prefix="/certificates", tags=["certificates"])

@app.get("/")
def root():
    return {
        "status": "Online",
        "product": "ZeroTrace",
        "message": "Secure Data Wiping Solution Backend Running"
    }
