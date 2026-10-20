from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field

class CategoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = None
class CategoryUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = None
class CategoryOut(BaseModel):
    id: int
    name: str
    description: str | None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class SupplierCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    email: str | None = None
    phone: str | None = None
    address: str | None = None
class SupplierUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=150)
    email: str | None = None
    phone: str | None = None
    address: str | None = None
class SupplierOut(BaseModel):
    id: int
    name: str
    email: str | None
    phone: str | None
    address: str | None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    description: str | None = None
    category_id: int
    supplier_id: int | None = None
    price: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    quantity: int = Field(default=0, ge=0)
class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = None
    category_id: int | None = None
    supplier_id: int | None = None
    price: Decimal | None = Field(default=None, gt=0, max_digits=10, decimal_places=2)
    quantity: int | None = Field(default=None, ge=0)
class ProductOut(BaseModel):
    id: int
    name: str
    description: str | None
    category_id: int
    supplier_id: int | None
    price: Decimal
    quantity: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
