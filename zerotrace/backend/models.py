from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    email = Column(String)
    name = Column(String)
    wipes_remaining = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"))
    wipes_added = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)


class WipeLog(Base):
    __tablename__ = "wipe_logs"

    id = Column(String, primary_key=True)
    user_id = Column(String)
    device_id = Column(String)
    status = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)


class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(String, primary_key=True)
    user_id = Column(String)
    device_info = Column(String)
    hash = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)