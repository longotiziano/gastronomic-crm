from app.models.raw_material import RawMaterial
from app.models.restaurant import Restaurant
from app.sql.database import Base 

from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Text, Float, ForeignKey

class StockMovement(Base):
    __tablename__ = "stock_movements"

    movement_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    r_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("restaurants.r_id"))
    rm_id: Mapped[int] = mapped_column(Integer, ForeignKey("raw_material.rm_id"), nullable=False)
    movement_amount: Mapped[float] = mapped_column(Float, nullable=False)
    movement_type: Mapped[Optional[str]] = mapped_column(Text)  # ej: 'entrada', 'salida', 'ajuste'
    movement_date: Mapped[Optional[str]] = mapped_column(Text, default="CURRENT_TIMESTAMP")
    movement_details: Mapped[Optional[str]] = mapped_column(Text)

    # relaciones
    restaurant: Mapped[Optional["Restaurant"]] = relationship(back_populates="stock_movements")
    raw_material: Mapped["RawMaterial"] = relationship(back_populates="stock_movements")

    def __repr__(self):
        return f"<StockMovement {self.movement_id} - rm:{self.rm_id} type:{self.movement_type} amount:{self.movement_amount}>"