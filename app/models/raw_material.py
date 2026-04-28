from app.models.raw_material_category import RawMaterialCategory
from app.models.recipe import Recipe
from app.models.restaurant import Restaurant
from app.models.stock import Stock
from app.models.stock_movement import StockMovement
from app.sql.database import Base 

from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Text, ForeignKey

class RawMaterial(Base):
    __tablename__ = "raw_material"

    rm_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rm_name: Mapped[str] = mapped_column(Text, nullable=False)
    rm_category: Mapped[int] = mapped_column(Integer, ForeignKey("raw_material_categories.rmc_id"), nullable=False)
    uom: Mapped[Optional[str]] = mapped_column(Text, default="grams")  # unit of measure
    r_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("restaurants.r_id"))

    # relaciones
    restaurant: Mapped[Optional["Restaurant"]] = relationship(back_populates="raw_materials")
    category: Mapped["RawMaterialCategory"] = relationship(back_populates="raw_materials")
    recipes: Mapped[list["Recipe"]] = relationship(back_populates="raw_material")
    stock: Mapped[list["Stock"]] = relationship(back_populates="raw_material")
    stock_movements: Mapped[list["StockMovement"]] = relationship(back_populates="raw_material")

    def __repr__(self):
        return f"<RawMaterial {self.rm_id} - {self.rm_name} ({self.uom})>"