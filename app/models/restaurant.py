from app.models.raw_material import RawMaterial
from app.models.recipe import Recipe
from app.models.sale import Sale
from app.models.stock import Stock
from app.models.stock_movement import StockMovement
from app.models.product import Product
from sql.database import Base 

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Text
from typing import Optional

class Restaurant(Base):
    __tablename__ = "restaurants"

    r_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    restaurant: Mapped[Optional[str]] = mapped_column(Text)

    # relaciones
    products: Mapped[list["Product"]] = relationship(back_populates="restaurant")
    raw_materials: Mapped[list["RawMaterial"]] = relationship(back_populates="restaurant")
    recipes: Mapped[list["Recipe"]] = relationship(back_populates="restaurant")
    sales: Mapped[list["Sale"]] = relationship(back_populates="restaurant")
    stock: Mapped[list["Stock"]] = relationship(back_populates="restaurant")
    stock_movements: Mapped[list["StockMovement"]] = relationship(back_populates="restaurant")

    def __repr__(self):
        """
        Modifies the way the class is printed in console
        """
        return f"<Restaurant {self.r_id} - {self.restaurant}>"




