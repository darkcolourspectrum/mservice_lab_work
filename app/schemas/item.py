
# Pydantic схемы для валидации входящих и исходящих данных

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ItemBase(BaseModel):

    name: str = Field(..., min_length=1, max_length=100, description="Название товара")
    description: Optional[str] = Field(None, max_length=500, description="Описание товара")
    price: float = Field(..., gt=0, description="Цена товара (должна быть больше 0)")
    is_available: bool = Field(True, description="Доступность товара")


class ItemCreate(ItemBase):
    pass 
    # наследуются все поля от ItemBase


class ItemUpdate(BaseModel):
    
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: Optional[float] = Field(None, gt=0)
    is_available: Optional[bool] = None
    # все поля опциональны


class ItemResponse(ItemBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        # Позволяет Pydantic работать с ORM моделями SQLAlchemy
        from_attributes = True