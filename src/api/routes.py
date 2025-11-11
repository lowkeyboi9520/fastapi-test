from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from src.infrastructure.database import get_db
from src.application.commands.product_commands import (
    CreateProductCommand, UpdateProductCommand, DeleteProductCommand
)
from src.application.queries.product_queries import (
    GetProductQuery, GetProductsQuery, SearchProductsQuery, ProductDTO
)
from src.application.handlers.product_handlers import (
    CreateProductHandler, UpdateProductHandler, DeleteProductHandler,
    GetProductHandler, GetProductsHandler, SearchProductsHandler
)

router = APIRouter()


@router.post("/products", response_model=ProductDTO, status_code=201)
async def create_product(
    command: CreateProductCommand,
    db: Session = Depends(get_db)
):
    handler = CreateProductHandler(db)
    return handler.handle(command)


@router.get("/products/{product_id}", response_model=ProductDTO)
async def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    handler = GetProductHandler(db)
    query = GetProductQuery(product_id=product_id)
    try:
        return handler.handle(query)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/products", response_model=list[ProductDTO])
async def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    category_id: int = Query(None, ge=0),
    is_active: bool = Query(True),
    db: Session = Depends(get_db)
):
    handler = GetProductsHandler(db)
    query = GetProductsQuery(
        skip=skip,
        limit=limit,
        category_id=category_id,
        is_active=is_active
    )
    return handler.handle(query)


@router.get("/products/search", response_model=list[ProductDTO])
async def search_products(
    query: str = Query(..., min_length=1, max_length=100),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    handler = SearchProductsHandler(db)
    search_query = SearchProductsQuery(
        query=query,
        skip=skip,
        limit=limit
    )
    return handler.handle(search_query)


@router.put("/products/{product_id}", response_model=ProductDTO)
async def update_product(
    product_id: int,
    command: UpdateProductCommand,
    db: Session = Depends(get_db)
):
    handler = UpdateProductHandler(db)
    try:
        return handler.handle(product_id, command)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/products/{product_id}")
async def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    handler = DeleteProductHandler(db)
    command = DeleteProductCommand(product_id=product_id)
    try:
        handler.handle(command)
        return {"message": "Product deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))