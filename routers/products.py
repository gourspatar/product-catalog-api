from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from schemas.product import Product, ProductCreate, ProductUpdate

from app.database import get_db
from app.models import Product as ProductModel

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
def get_products(db: Session = Depends(get_db)):
    return db.query(ProductModel).all()

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
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
):
    new_product = ProductModel(
        name=product.name,
        description=product.description,
        price=product.price,
        category_id=product.category_id,
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

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