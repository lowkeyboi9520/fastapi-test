from sqlalchemy.orm import Session
from src.domain.models.product import Product
from typing import List, Optional


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, product_data: dict) -> Product:
        product = Product(**product_data)
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def get_by_id(self, product_id: int) -> Optional[Product]:
        return self.db.query(Product).filter(Product.id == product_id).first()

    def get_by_sku(self, sku: str) -> Optional[Product]:
        return self.db.query(Product).filter(Product.sku == sku).first()

    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        category_id: Optional[int] = None,
        is_active: bool = True
    ) -> List[Product]:
        query = self.db.query(Product)

        if category_id:
            query = query.filter(Product.category_id == category_id)

        if is_active:
            query = query.filter(Product.is_active == True)

        return query.offset(skip).limit(limit).all()

    def update(self, product_id: int, product_data: dict) -> Optional[Product]:
        product = self.get_by_id(product_id)
        if product:
            for key, value in product_data.items():
                setattr(product, key, value)
            self.db.commit()
            self.db.refresh(product)
        return product

    def delete(self, product_id: int) -> bool:
        product = self.get_by_id(product_id)
        if product:
            self.db.delete(product)
            self.db.commit()
            return True
        return False

    def search(self, query: str, skip: int = 0, limit: int = 20) -> List[Product]:
        return self.db.query(Product).filter(
            Product.name.ilike(f"%{query}%") |
            Product.description.ilike(f"%{query}%")
        ).offset(skip).limit(limit).all()