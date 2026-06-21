from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr

# --- প্রোডাক্ট স্কিমাস ---
class ProductResponse(BaseModel):
    id: int
    title: str
    price: int
    is_available: bool
    model_config = ConfigDict(from_attributes=True) 

class ProductCreateUpdate(BaseModel):
    title: str
    price: int
    is_available: bool = True
    model_config = ConfigDict(
        json_schema_extra={"example": {"title": "Smart Watch", "price": 2500, "is_available": True}}
    )

# --- বুক স্কিমাস ---
class BookResponse(BaseModel):
    id: int
    name: str
    price: float
    model_config = ConfigDict(from_attributes=True)

class BookCreateUpdate(BaseModel):
    name: str
    price: float
    model_config = ConfigDict(
        json_schema_extra={"example": {"name": "The Alchemist", "price": 350.0}}
    )
# --- ইউজার স্কিমাস ---

class UserCreate(BaseModel):
    email: EmailStr  
    password: str
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "password": "securepassword123"
            }
        }
    )

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# ==========================================
# 🔐 অথেনটিকেশন / টোকেন স্কিমা (নতুন যোগ করুন)
# ==========================================

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None

