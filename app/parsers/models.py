from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from baseclass import Base

class Platform(Base):
    __tablename__ = "platforms"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    games = relationship("Game", back_populates="platform")

class Game(Base):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, index=True, nullable=False)
    platform_id: Mapped[int] = mapped_column(ForeignKey("platforms.id"), index=True, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=True)
    availability: Mapped[bool] = mapped_column(Boolean, default=True)
    store_id: Mapped[int] = mapped_column(ForeignKey("stores.id"))

    platform = relationship("Platform", back_populates="games")  # <-- ДОБАВЛЕНО
    store = relationship("Store", back_populates="games")

class Store(Base):
    __tablename__ = "stores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    games = relationship("Game", back_populates="store")

class User(Base):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True, index=True)
    email = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password = mapped_column(String, nullable=False)
    is_active = mapped_column(Boolean, default=True)
