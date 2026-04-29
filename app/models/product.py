from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:    
    from app.models.recipe import Recipe
    from app.models.restaurant import Restaurant
    from app.models.product_category import ProductCategory
    from app.models.sale import Sale
from app.sql.database import Base 


from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Text, Float, ForeignKey

class Product(Base):
    __tablename__ = "products"

    product_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    r_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("restaurants.r_id"))
    category_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("products_categories.category_id"))
    product_name: Mapped[str] = mapped_column(Text, nullable=False)
    product_type: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False, default=0)

    # relaciones
    restaurant: Mapped[Optional["Restaurant"]] = relationship(back_populates="products")
    category: Mapped[Optional["ProductCategory"]] = relationship(back_populates="products")
    recipes: Mapped[list["Recipe"]] = relationship(back_populates="product")
    sales: Mapped[list["Sale"]] = relationship(back_populates="product")

    def __repr__(self):
        return f"<Product {self.product_id} - {self.product_name}>"
    
    def _to_dict(self) -> dict:
        """
        Returns the conventional dictionary that will use the frontend
        """
        return {
            "product_name": self.product_name,
            "product_category": self.category.category_name if self.category else None,
            "price": self.price,
            "recipes": None # for now
        }