from fastapi import APIRouter, HTTPException, status

from schemas.category import Category, CategoryCreate, CategoryUpdate


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
def get_categories():
    return categories


@router.get("/{category_id}", response_model=Category)
def get_category(category_id: int):
    for category in categories:
        if category["id"] == category_id:
            return category

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Category not found",
    )


@router.post(
    "/",
    response_model=Category,
    status_code=status.HTTP_201_CREATED,
)
def create_category(category: CategoryCreate):
    new_id = max((item["id"] for item in categories), default=0) + 1

    new_category = {
        "id": new_id,
        **category.model_dump(),
    }

    categories.append(new_category)

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