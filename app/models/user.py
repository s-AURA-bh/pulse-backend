from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    tasks = relationship(
        "Task",
        back_populates="user",
        cascade="all, delete-orphan",
    )
  
    goals = relationship(
        "Goal",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    notes = relationship(
        "Note",
        back_populates="user",
        cascade="all, delete-orphan",
    )
