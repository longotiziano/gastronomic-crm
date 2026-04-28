from app.models.raw_material import RawMaterial
from app.sql.database import Base 

from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Text

class RawMaterialCategory(Base):
    __tablename__ = "raw_material_categories"

    rmc_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rmc_name: Mapped[str] = mapped_column(Text, nullable=False)
    rmc_section: Mapped[Optional[str]] = mapped_column(Text)

    # relaciones
    raw_materials: Mapped[list["RawMaterial"]] = relationship(back_populates="category")

    def __repr__(self):
        return f"<RawMaterialCategory {self.rmc_id} - {self.rmc_name}>"