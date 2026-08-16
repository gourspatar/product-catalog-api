from fastapi import FastAPI
from routers import products, categories
from app.database import engine, Base
from app import models

    
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Product Catalog API",
    description="A professional REST API for managing products and categories.",
    version="1.0.0",
)


app.include_router(products.router)
app.include_router(categories.router)


@app.get("/")
def root():
    return {
        "message": "Product Catalog API is running",
        "docs": "/docs",
        "version": "1.0.0",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}