from app.models.raw_material import RawMaterial
from app.models.restaurant import Restaurant
from app.sql.database import Base 


from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Text, Float, ForeignKey, CheckConstraint

class Stock(Base):
    __tablename__ = "stock"

    # clave primaria compuesta (r_id + rm_id)
    r_id: Mapped[int] = mapped_column(Integer, ForeignKey("restaurants.r_id"), primary_key=True)
    rm_id: Mapped[int] = mapped_column(Integer, ForeignKey("raw_material.rm_id"), primary_key=True)
    stock_amount: Mapped[float] = mapped_column(Float, nullable=False, default=0)

    # relaciones
    restaurant: Mapped["Restaurant"] = relationship(back_populates="stock")
    raw_material: Mapped["RawMaterial"] = relationship(back_populates="stock")

    def __repr__(self):
        return f"<Stock r:{self.r_id} rm:{self.rm_id} amount:{self.stock_amount}>"