from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from schemas.product import Product, ProductCreate, ProductUpdate

from app.database import get_db
from app.models import Product as ProductModel

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.get("/", response_model=list[Product])
def get_products(db: Session = Depends(get_db)):
    return db.query(ProductModel).all()

@router.get("/{product_id}", response_model=Product)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    product = db.query(ProductModel).filter(
        ProductModel.id == product_id
    ).first()

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    return product


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
def update_product(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db),
):
    existing_product = db.query(ProductModel).filter(
        ProductModel.id == product_id
    ).first()

    if existing_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    update_data = product.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(existing_product, field, value)

    db.commit()
    db.refresh(existing_product)

    return existing_product

@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    product = db.query(ProductModel).filter(
        ProductModel.id == product_id
    ).first()

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    db.delete(product)
    db.commit()

    return {
        "message": "Product deleted successfully",
        "product_id": product_id,
    }