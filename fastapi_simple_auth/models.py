import uuid
from sqlalchemy import Boolean, Integer, Column, String, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

Base = declarative_base()

def get_uuid():
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"

    uuid = Column(String(36), nullable=False, unique=True, primary_key=True, default=get_uuid)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    created = Column(DateTime)
    last_login = Column(DateTime)
    admin_comment = Column(String)
    email_verified = Column(Boolean, default=False)
    disabled = Column(Boolean, default=False)
    other = Column(Text)
    codes = relationship("Code", back_populates="user")

    def __repr__(self):
        return f"user #{self.uuid} usename:{self.username} {self.email}"


class Code(Base):
    __tablename__ = "codes"

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)

    user_id = Column(String(36), ForeignKey("users.uuid"))

    code = Column(String)
    purpose = Column(String)
    created = Column(DateTime(timezone=True), server_default=func.now())
    expires = Column(DateTime(timezone=True))
    user = relationship("User", back_populates="codes")