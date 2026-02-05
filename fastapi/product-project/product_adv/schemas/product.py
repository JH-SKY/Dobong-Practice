from pydantic import BaseModel, Field, field_validator, ValidationInfo


class Product:
    def __init__(self, name, price, discount_price, stock, category):
        self.id = None
        self.name = name
        self.price = price
        self.discount_price = discount_price
        self.stock = stock
        self.category = category


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, alias="product_name")
    price: int = Field(..., ge=100)
    discount_price: int = Field(..., ge=0)
    stock: int = Field(default=10, ge=0)
    category: str = Field(..., min_length=2)

    @field_validator("discount_price")
    @classmethod
    def check_discount_less_than_price(cls, v: int, info: ValidationInfo) -> int:
        if "price" in info.data and v >= info.data["price"]:
            raise ValueError("discout가 price보다 높아서는 안되.")
        return v


class ProductDetailResponse(BaseModel):
    id: int
    name: str
    final_price: int
    category: str
    is_soldout: bool
    stock: int


class ProductListResponse(BaseModel):
    id: int
    name: str
    final_price: int
    category: str
