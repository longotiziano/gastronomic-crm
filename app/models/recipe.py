from app.models.raw_material import RawMaterial
from app.models.restaurant import Restaurant
from app.models.product import Product
from app.sql.database import Base 

from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Text, Float, ForeignKey

class Recipe(Base):
    __tablename__ = "recipes"

    recipe_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    r_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("restaurants.r_id"))
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.product_id"), nullable=False)
    rm_id: Mapped[int] = mapped_column(Integer, ForeignKey("raw_material.rm_id"), nullable=False)
    rm_amount: Mapped[float] = mapped_column(Float, nullable=False)
    waste: Mapped[Optional[float]] = mapped_column(Float, default=0)

    # relaciones
    restaurant: Mapped[Optional["Restaurant"]] = relationship(back_populates="recipes")
    product: Mapped["Product"] = relationship(back_populates="recipes")
    raw_material: Mapped["RawMaterial"] = relationship(back_populates="recipes")

    # cantidad Float considerando el desperdicio
    @property
    def rm_amount_with_waste(self) -> float:
        return self.rm_amount * (1 + (self.waste or 0))

    def __repr__(self):
        return f"<Recipe {self.recipe_id} - product:{self.product_id} rm:{self.rm_id}>"