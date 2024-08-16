from typing import Generator
from sqlalchemy.orm import Session
from src.infrastructures.databases.database import postgres


def get_sample_db() -> Generator[Session, None, None]:
    db: Session = postgres("belajar")
    try:
        yield db
    finally:
        db.close()
