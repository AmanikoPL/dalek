from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.baseclass import Base

class Game(Base):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, index=True, nullable=False)
    platform: Mapped[str] = mapped_column(String, index=True, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=True)
    availability: Mapped[bool] = mapped_column(Boolean, default=True)
    store_id: Mapped[int] = mapped_column(ForeignKey("stores.id"))

    store = relationship("Store", back_populates="games")
