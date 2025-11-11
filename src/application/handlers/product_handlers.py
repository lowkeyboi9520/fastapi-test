from sqlalchemy.orm import Session
from src.application.commands.product_commands import CreateProductCommand, UpdateProductCommand, DeleteProductCommand
from src.application.queries.product_queries import ProductDTO, GetProductQuery, GetProductsQuery, SearchProductsQuery
from src.infrastructure.repositories.product_repository import ProductRepository
from src.domain.models.product import Product
from typing import List
from datetime import datetime


class CreateProductHandler:
    def __init__(self, db: Session):
        self.product_repository = ProductRepository(db)

    def handle(self, command: CreateProductCommand) -> ProductDTO:
        product_data = command.model_dump()
        product = self.product_repository.create(product_data)
        return ProductDTO.model_validate(product)


class UpdateProductHandler:
    def __init__(self, db: Session):
        self.product_repository = ProductRepository(db)

    def handle(self, product_id: int, command: UpdateProductCommand) -> ProductDTO:
        update_data = command.model_dump(exclude_unset=True)
        product = self.product_repository.update(product_id, update_data)
        if not product:
            raise ValueError(f"Product with id {product_id} not found")
        return ProductDTO.model_validate(product)


class DeleteProductHandler:
    def __init__(self, db: Session):
        self.product_repository = ProductRepository(db)

    def handle(self, command: DeleteProductCommand) -> bool:
        success = self.product_repository.delete(command.product_id)
        if not success:
            raise ValueError(f"Product with id {command.product_id} not found")
        return success


class GetProductHandler:
    def __init__(self, db: Session):
        self.product_repository = ProductRepository(db)

    def handle(self, query: GetProductQuery) -> ProductDTO:
        product = self.product_repository.get_by_id(query.product_id)
        if not product:
            raise ValueError(f"Product with id {query.product_id} not found")
        return ProductDTO.model_validate(product)


class GetProductsHandler:
    def __init__(self, db: Session):
        self.product_repository = ProductRepository(db)

    def handle(self, query: GetProductsQuery) -> List[ProductDTO]:
        products = self.product_repository.get_all(
            skip=query.skip,
            limit=query.limit,
            category_id=query.category_id,
            is_active=query.is_active
        )
        return [ProductDTO.model_validate(product) for product in products]


class SearchProductsHandler:
    def __init__(self, db: Session):
        self.product_repository = ProductRepository(db)

    def handle(self, query: SearchProductsQuery) -> List[ProductDTO]:
        products = self.product_repository.search(
            query=query.query,
            skip=query.skip,
            limit=query.limit
        )
        return [ProductDTO.model_validate(product) for product in products]