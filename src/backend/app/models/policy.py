from __future__ import annotations

from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.client import Client
    from app.models.management_action import ManagementAction


class Policy(Base):
    """SQLAlchemy model for insurance policies."""

    __tablename__ = "policies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    client_id: Mapped[int] = mapped_column(
        ForeignKey("clients.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    insurer: Mapped[str] = mapped_column(String(100), nullable=False)
    policy_type: Mapped[str] = mapped_column(String(20), nullable=False)
    policy_number: Mapped[str | None] = mapped_column(
        String(100),
        unique=True,
        nullable=True,
    )
    expiration_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="active",
        server_default="active",
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    client: Mapped[Client] = relationship("Client", back_populates="policies")
    management_actions: Mapped[list[ManagementAction]] = relationship(
        "ManagementAction",
        back_populates="policy",
    )
