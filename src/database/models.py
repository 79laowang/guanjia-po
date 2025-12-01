from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional

@dataclass
class Category:
    id: Optional[int] = None
    name: str = ""
    type: str = ""  # 'income' or 'expense'
    color: str = "#1890ff"
    created_at: Optional[datetime] = None

@dataclass
class Account:
    id: Optional[int] = None
    type: str = ""  # 'income' or 'expense'
    amount: float = 0.0
    category_id: int = 0
    category_name: Optional[str] = None
    category_color: Optional[str] = None
    description: str = ""
    date: date = date.today()
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

@dataclass
class ItemCategory:
    id: Optional[int] = None
    name: str = ""
    description: Optional[str] = None
    created_at: Optional[datetime] = None

@dataclass
class Item:
    id: Optional[int] = None
    name: str = ""
    category_id: Optional[int] = None
    category_name: Optional[str] = None
    quantity: float = 0.0
    unit: str = "个"
    unit_price: float = 0.0
    min_quantity: float = 0.0
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

@dataclass
class InventoryTransaction:
    id: Optional[int] = None
    item_id: int = 0
    item_name: Optional[str] = None
    category_name: Optional[str] = None
    type: str = ""  # 'in' or 'out'
    quantity: float = 0.0
    unit_price: float = 0.0
    reason: Optional[str] = None
    date: date = date.today()
    created_at: Optional[datetime] = None

@dataclass
class AccountSummary:
    type: str
    total: float
    count: int

@dataclass
class CategorySummary:
    name: str
    color: str
    total: float
    count: int