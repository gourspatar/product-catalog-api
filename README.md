# Product Catalog API

A professional RESTful API for managing products and categories, built with **FastAPI** and **Pydantic**.

This project demonstrates clean API structure, request validation, CRUD operations, HTTP error handling, and automatic OpenAPI documentation.

## 🚀 Features

- Product CRUD operations
- Category CRUD operations
- Request and response validation with Pydantic
- Proper HTTP status codes
- Resource-level error handling
- Automatic Swagger/OpenAPI documentation
- Health check endpoint
- Clean separation of application, routing, and schema layers
- API versioning through application metadata

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Backend programming |
| FastAPI | REST API framework |
| Pydantic | Data validation and schemas |
| Uvicorn | ASGI server |
| Swagger / OpenAPI | Interactive API documentation |

## 📁 Project Structure

```text
product-catalog-api/
│
├── app/
│   ├── __init__.py
│   └── main.py
│
├── routers/
│   ├── __init__.py
│   ├── products.py
│   └── categories.py
│
├── schemas/
│   ├── __init__.py
│   ├── product.py
│   └── category.py
│
├── .gitignore
├── README.md
└── requirements.txt