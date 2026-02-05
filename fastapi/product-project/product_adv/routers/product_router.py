from fastapi import APIRouter, status, Path, Query
from product_adv.schemas.product import ProductCreate, ProductDetailResponse, ProductListResponse
from product_adv.services.product_service import product_service
from typing import Annotated

router = APIRouter(prefix="/product-adv")


# 클라이언트로부터 데이터를 입력받아서 저장하는 역할.
# 어떤 데이터를 입력받지? -> ProductCreate
@router.post("", status_code=status.HTTP_201_CREATED)
def create_product(data: ProductCreate):
    return product_service.create_product(data)


@router.get("/{id}", response_model=ProductDetailResponse)
def read_product_by_id(id: Annotated[int, Path(ge=1)]):
    return product_service.read_product_by_id(id)

# products?keyword=value&p-category=value&...
@router.get("", response_model=list[ProductListResponse])
def read_products(
    keyword: Annotated[str | None, Query(min_length=2)] = None,
    category: Annotated[str | None, Query(alias="p-category")] = None,
    limit: Annotated[int, Query()] = 20
):
    return product_service.read_products(keyword, category, limit)

