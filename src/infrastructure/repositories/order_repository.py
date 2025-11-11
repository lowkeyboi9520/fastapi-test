from sqlalchemy.orm import Session
from src.domain.models.order import Order, OrderItem
from typing import List, Optional
from datetime import datetime
import uuid


class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, order_data: dict) -> Order:
        # Generate unique order number
        order_number = f"ORD-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
        order_data['order_number'] = order_number

        order = Order(**order_data)
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order

    def get_by_id(self, order_id: int) -> Optional[Order]:
        return self.db.query(Order).filter(Order.id == order_id).first()

    def get_by_order_number(self, order_number: str) -> Optional[Order]:
        return self.db.query(Order).filter(Order.order_number == order_number).first()

    def get_by_user_id(self, user_id: int, skip: int = 0, limit: int = 20) -> List[Order]:
        return self.db.query(Order).filter(Order.user_id == user_id).offset(skip).limit(limit).all()

    def get_all(self, skip: int = 0, limit: int = 100, status: Optional[str] = None) -> List[Order]:
        query = self.db.query(Order)

        if status:
            query = query.filter(Order.status == status)

        return query.offset(skip).limit(limit).all()

    def update_status(self, order_id: int, status: str) -> Optional[Order]:
        order = self.get_by_id(order_id)
        if order:
            order.status = status
            self.db.commit()
            self.db.refresh(order)
        return order

    def add_item(self, order_id: int, item_data: dict) -> OrderItem:
        item_data['order_id'] = order_id
        item = OrderItem(**item_data)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def update_item(self, item_id: int, item_data: dict) -> Optional[OrderItem]:
        item = self.db.query(OrderItem).filter(OrderItem.id == item_id).first()
        if item:
            for key, value in item_data.items():
                setattr(item, key, value)
            self.db.commit()
            self.db.refresh(item)
        return item

    def delete_item(self, item_id: int) -> bool:
        item = self.db.query(OrderItem).filter(OrderItem.id == item_id).first()
        if item:
            self.db.delete(item)
            self.db.commit()
            return True
        return False