from pydantic import BaseModel, Field, ConfigDict

from schemas.category import Category


class ProductBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    price: float = Field(..., gt=0)
    category_id: int = Field(..., gt=0)


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int
    category: Category

    model_config = ConfigDict(from_attributes=True)


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    price: float | None = Field(default=None, gt=0)
    category_id: int | None = Field(default=None, gt=0)