from typing import List, Optional

from sqlalchemy.orm import Session

try:
    from .models import Fishing
except ImportError:  # Allow running as a script (python main.py)
    from models import Fishing


def list_fishings(db: Session, iin: Optional[str]) -> List[Fishing]:
    if iin is not None:
        return db.query(Fishing).filter(Fishing.iin == iin).all()
    return db.query(Fishing).all()


def save_fishing(db: Session, fishing: Fishing) -> None:
    db.add(fishing)
    db.commit()
    db.refresh(fishing)


def delete_fishing(db: Session, fishing_id: int) -> None:
    db.query(Fishing).filter(Fishing.id == fishing_id).delete()
    db.commit()


def get_fishing_by_id(db: Session, fishing_id: int) -> Optional[Fishing]:
    return db.query(Fishing).filter(Fishing.id == fishing_id).first()
