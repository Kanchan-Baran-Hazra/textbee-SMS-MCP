from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .main import Base


class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
    )

    textbee_device_id: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
    )

    textbee_api_key: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
    )

    scopes: Mapped[str] = mapped_column(
        String(500),
        default="profile:read",
    )