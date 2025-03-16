# from sqlalchemy import Integer, String
# from sqlalchemy.orm import Mapped, mapped_column, relationship
# from app.models.baseclass import Base

# class Platform(Base):  # Исправил название класса для логики
#     __tablename__ = "platforms"

#     id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
#     name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

#     games = relationship("Game", back_populates="platform")
