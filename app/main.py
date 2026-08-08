from fastapi import FastAPI


app = FastAPI(
    title="Product Catalog API",
    description="REST API for managing products and categories.",
    version="1.0.0",
)


@app.get("/")
def health_check():
    return {"message": "Product Catalog API is running"}