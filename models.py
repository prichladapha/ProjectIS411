from pydantic import BaseModel
from sqlmodel import Field, SQLModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

#Product
class Product(BaseModel):
    pname: str
    price: float | None = None
    brand: str
    description: str
    categoryID: int
    seller_id: int
    tags: str
    product_status: str = "available"

class ProductOut(Product):
    product_id: int

class ProductDB(SQLModel, table=True):
    product_id:int | None = Field(default=None, primary_key=True)
    pname: str
    price: float | None = None
    brand: str
    description: str
    categoryID: int
    seller_id: int
    tags: str
    product_status: str = "available"

#Order
class OrderStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    paid = "paid"
    shipping = "shipping"
    delivered = "delivered"
    cancelled = "cancelled"

class Order(BaseModel):
    cus_id: int
    total_price: float
    shipping_cost: float = 50
    order_status: OrderStatus = OrderStatus.pending

class OrderDB(SQLModel, table=True):
    order_id: int | None = Field(default=None, primary_key=True)
    cus_id: int
    total_price: float
    shipping_cost: float = 50
    grand_total: float
    order_status: OrderStatus = OrderStatus.pending
    created_at: datetime = Field(default_factory=datetime.now)

class OrderOut(Order):
    order_id: int
    cus_id: int
    total_price: float
    shipping_cost: float
    grand_total: float
    order_status: OrderStatus
    created_at: datetime

#OrderItem
class OrderItem(BaseModel):
    order_id: int
    product_id: int
    qty: int
    price: float

class OrderItemDB(SQLModel, table=True):
    orderitem_id: int | None = Field(default=None, primary_key=True)
    order_id: int
    product_id: int 
    qty: int
    price: float

class OrderItemCreate(BaseModel):
    product_id: int
    qty: int = Field(gt=0, description="Quantity must be greater than 0")

class OrderCreate(BaseModel):
    cus_id: int
    items: List[OrderItemCreate] 
    shipping_cost: float = 50

class OrderItemOut(OrderItem):
    orderitem_id: int

#Category
class Category(BaseModel):
    category_name: str

class CategoryDB(SQLModel, table=True):
    category_id: int | None = Field(default=None, primary_key=True)
    category_name: str


#Payment
class Payment(BaseModel):
    order_id: int
    payment_method: str
    payment_amount: float
    payment_status: str
    payment_date: str
    transaction_no: str

class PaymentOut(Payment):
    payment_id: int
 
class PaymentDB(SQLModel, table=True):
    payment_id: int | None = Field(default=None, primary_key=True)
    order_id: int
    payment_method: str
    payment_amount: float
    payment_status: str
    payment_date: str
    transaction_no: int

#Customer
class Customer(BaseModel):
    username: str
    email: str
    customer_phone: str

class CustomerOut(Customer):
    customer_id: int

class CustomerDB(SQLModel, table=True):
    customer_id: int | None = Field(default=None, primary_key=True)
    username: str
    email: str
    customer_phone: str

#Address  
class Address(BaseModel):
    cus_id: int
    address_line: str
    district: str
    province: str
    postal_code: str
    address_type: str

class AddressDB(SQLModel, table=True):
    address_id: int | None = Field(default=None, primary_key=True)
    cus_id: int
    address_line: str
    district: str
    province: str
    postal_code: str
    address_type: str

#Shipment
class Shipment(BaseModel):
    order_id : int
    address_id : int
    carrier : str
    tracking_no : int
    shipment_status : str

class ShipmentDB(SQLModel, table=True):
    shipment_id: int | None = Field(default=None, primary_key=True)
    order_id : int
    address_id : int
    carrier : str
    tracking_no : int
    shipment_status : str

#Seller   
class Seller(BaseModel):
    seller_name : str
    email : str
    seller_phone : str
    store_name : str
    verification_status : str
    
class SellerOut(Seller):
    seller_id: int

class SellerDB(SQLModel, table=True):
    seller_id : int | None = Field(default=None, primary_key=True)
    seller_name : str
    email : str
    seller_phone : str
    store_name : str
    verification_status : str

###search
class SortBy(str, Enum):
    PRICE_LOW = "price_low"
    PRICE_HIGH = "price_high"
    NEWEST = "newest"
    OLDEST = "oldest"
    
class ProductSearchRequest(BaseModel):
    """Schema สำหรับ Search Request"""
    
    # Text Search
    query: Optional[str] = Field(None, description="ค้นหาจากชื่อสินค้า, brand, description")
    
    # Filters
    category_id: Optional[int] = None
    brand: Optional[str] = None
    tags: Optional[List[str]] = Field(None, description="เช่น ['streetwear', 'vintage']")
    
    # Price Range (ถ้าอยากมี)
    min_price: Optional[float] = Field(None, ge=0)
    max_price: Optional[float] = Field(None, ge=0)
    
    # Sorting
    sort_by: Optional[SortBy] = Field(SortBy.NEWEST, description="การเรียงลำดับ")
    
    # Pagination
    page: int = Field(1, ge=1, description="หน้าที่ต้องการ")
    page_size: int = Field(20, ge=1, le=100, description="จำนวนสินค้าต่อหน้า")              