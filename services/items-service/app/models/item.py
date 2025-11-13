# ORM модель для таблицы items в базе

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.sql import func

from app.db.database import Base


class Item(Base):
    
    __tablename__ = "items" 
    
    id = Column(Integer, primary_key=True, index=True) # первичный, автоинкрементный ключ
    
    name = Column(String, nullable=False, index=True) # обязательное поле с названием товара
     
    description = Column(String, nullable=True) # описание товара, может быть пустым
    
    price = Column(Float, nullable=False) # цена товара
    
    is_available = Column(Boolean, default=True) # доступность товара
    
    # временные метки
    created_at = Column(DateTime(timezone=True), server_default=func.now()) # время на стороне бд
    updated_at = Column(DateTime(timezone=True), server_default=None, onupdate=func.now())