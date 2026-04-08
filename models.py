from sqlalchemy import Column, Integer, String

try:
    from .db import Base
except ImportError:  # Allow running as a script (python main.py)
    from db import Base


class Fishing(Base):
    __tablename__ = "fishings"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    iin = Column(String, nullable=True)
    password = Column(String, nullable=True)
