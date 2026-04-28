from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:    
    from app.models.restaurant import Restaurant
    from app.models.product import Product
from app.sql.database import Base 

from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Text, Float, ForeignKey

class Sale(Base):
    __tablename__ = "sales"

    sale_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    r_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("restaurants.r_id"))
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.product_id"), nullable=False)
    sale_quantity: Mapped[float] = mapped_column(Float, nullable=False)
    sale_date: Mapped[Optional[str]] = mapped_column(Text, default="CURRENT_TIMESTAMP")
    sale_details: Mapped[Optional[str]] = mapped_column(Text)

    # relaciones
    restaurant: Mapped[Optional["Restaurant"]] = relationship(back_populates="sales")
    product: Mapped["Product"] = relationship(back_populates="sales")

    @property
    def total(self) -> float:
        return self.sale_quantity * (self.product.price if self.product else 0)

    def __repr__(self):
        return f"<Sale {self.sale_id} - product:{self.product_id} qty:{self.sale_quantity}>"