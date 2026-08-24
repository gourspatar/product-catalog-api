from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from schemas.category import Category, CategoryCreate, CategoryUpdate

from app.database import get_db
from app.models import Category as CategoryModel


router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)


categories = [
    {
        "id": 1,
        "name": "Electronics",
        "description": "Electronic products and accessories",
    },
    {
        "id": 2,
        "name": "Accessories",
        "description": "Computer and mobile accessories",
    },
]


@router.get("/", response_model=list[Category])
def get_categories(db: Session = Depends(get_db)):
    return db.query(CategoryModel).all()


@router.get("/{category_id}", response_model=Category)
def get_category(
    category_id: int,
    db: Session = Depends(get_db),
):
    category = db.query(CategoryModel).filter(
        CategoryModel.id == category_id
    ).first()

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    return category

@router.post(
    "/",
    response_model=Category,
    status_code=status.HTTP_201_CREATED,
)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
):
    new_category = CategoryModel(
        name=category.name,
        description=category.description,
    )

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category


@router.put("/{category_id}", response_model=Category)
def update_category(category_id: int, category: CategoryUpdate):
    for existing_category in categories:
        if existing_category["id"] == category_id:
            update_data = category.model_dump(exclude_unset=True)

            existing_category.update(update_data)

            return existing_category

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Category not found",
    )


@router.delete("/{category_id}")
def delete_category(category_id: int):
    for index, category in enumerate(categories):
        if category["id"] == category_id:
            categories.pop(index)

            return {
                "message": "Category deleted successfully",
                "category_id": category_id,
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Category not found",
    )