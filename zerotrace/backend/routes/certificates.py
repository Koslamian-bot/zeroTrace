from fastapi import APIRouter
import hashlib
import uuid
from datetime import datetime

router = APIRouter()

blockchain = []

@router.post("/upload-certificate")
def upload_certificate(data: dict):
    cert_str = str(data)
    cert_hash = hashlib.sha256(cert_str.encode()).hexdigest()

    block = {
        "id": str(uuid.uuid4()),
        "hash": cert_hash,
        "timestamp": str(datetime.utcnow())
    }

    blockchain.append(block)

    return {
        "certificate_hash": cert_hash,
        "block_id": block["id"]
    }