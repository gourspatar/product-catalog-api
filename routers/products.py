from fastapi import APIRouter, HTTPException, status

from schemas.product import Product, ProductCreate, ProductUpdate


router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


products = [
    {
        "id": 1,
        "name": "Wireless Mouse",
        "description": "Ergonomic wireless mouse",
        "price": 799.00,
        "category_id": 1,
    },
    {
        "id": 2,
        "name": "Mechanical Keyboard",
        "description": "RGB mechanical keyboard",
        "price": 2499.00,
        "category_id": 1,
    },
]


@router.get("/", response_model=list[Product])
def get_products():
    return products


@router.get("/{product_id}", response_model=Product)
def get_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return product

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Product not found",
    )


@router.post(
    "/",
    response_model=Product,
    status_code=status.HTTP_201_CREATED,
)
def create_product(product: ProductCreate):
    new_id = max((item["id"] for item in products), default=0) + 1

    new_product = {
        "id": new_id,
        **product.model_dump(),
    }

    products.append(new_product)

    return new_product


@router.put("/{product_id}", response_model=Product)
def update_product(product_id: int, product: ProductUpdate):
    for existing_product in products:
        if existing_product["id"] == product_id:
            update_data = product.model_dump(exclude_unset=True)

            existing_product.update(update_data)

            return existing_product

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Product not found",
    )


@router.delete("/{product_id}")
def delete_product(product_id: int):
    for index, product in enumerate(products):
        if product["id"] == product_id:
            products.pop(index)

            return {
                "message": "Product deleted successfully",
                "product_id": product_id,
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Product not found",
    )