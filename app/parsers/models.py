from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.parsers.baseclass import Base
from typing import Optional

class Platform(Base):
    __tablename__ = "platforms"
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    games = relationship("Game", back_populates="platform")

class Game(Base):
    __tablename__ = "games"
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    platform_id: Mapped[int] = mapped_column(ForeignKey("platforms.id", ondelete="CASCADE"), index=True, nullable=False)
    price: Mapped[Optional[int]] = mapped_column(Integer)
    availability: Mapped[bool] = mapped_column(Boolean, default=True)
    store_id: Mapped[int] = mapped_column(ForeignKey("stores.id", ondelete="SET NULL"), nullable=True)
    image_url: Mapped[Optional[str]] = mapped_column(Text)
    url: Mapped[Optional[str]] = mapped_column(Text)  # <-- новое поле
    reserved_by_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    reserved_by = relationship("User")

    platform: Mapped["Platform"] = relationship("Platform", back_populates="games")
    store: Mapped["Store"] = relationship("Store", back_populates="games")

class Store(Base):
    __tablename__ = "stores"
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    games = relationship("Game", back_populates="store")

class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    id = mapped_column(Integer, primary_key=True, index=True)
    email = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password = mapped_column(String, nullable=False)
    is_active = mapped_column(Boolean, default=True)
