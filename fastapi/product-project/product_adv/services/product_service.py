from product_adv.schemas.product import ProductCreate, Product
from product_adv.repositories.product_repository import product_repository
from fastapi import HTTPException, status


class ProductService:
    def create_product(self, data: ProductCreate):
        new_product = Product(
            name=data.name,
            price=data.price,
            discount_price=data.discount_price,
            stock=data.stock,
            category=data.category,
        )
        return product_repository.save(new_product)

    def read_product_by_id(self, id: int):
        product = product_repository.find_by_id(id)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        # product: Product
        # return: ProductDetail에 해당하는 값

        # if product.stock:  # 없다 즉 0, "", [] => false로 처리
        #     is_soldout = False
        # else:
        #     is_soldout = True
        # # 삼항연산자.
        # is_soldout = False if product.stock else True

        return {
            "id": product.id,
            "name": product.name,
            "final_price": product.price - product.discount_price,
            "category": product.category,
            "is_soldout": False if product.stock else True,
            "stock": product.stock,
        }

    def read_products(self, keyword: str, category: str, limit: int):
        # 레포지토리에서 products를 가져온다.
        # keyword에 해당하는 product만 필터링
        # category에 해당하는 product만 필터링
        # limit개만큼만 가져올겁니다.
        # products = product_repository.find_all()
        # service에서 필터링을 할수도 있겠찌만

        products = product_repository.find_all_with_keyword_category_limit(
            keyword, category, limit
        )
        # Product -> ProductListREsponse

        results = []

        for product in products:
            results.append(
                {
                    "id": product.id,
                    "name": product.name,
                    "final_price": product.price - product.discount_price,
                    "category": product.category,
                }
            )
        return results


product_service = ProductService()
