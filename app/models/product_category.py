from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.product import Product
from app.sql.database import Base 

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Text

class ProductCategory(Base):
    __tablename__ = "products_categories"

    category_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category_name: Mapped[str] = mapped_column(Text, nullable=False)
    category_type: Mapped[str] = mapped_column(Text, nullable=False)

    # relaciones
    products: Mapped[list["Product"]] = relationship(back_populates="category")

    def __repr__(self):
        return f"<ProductCategory {self.category_id} - {self.category_name}>"