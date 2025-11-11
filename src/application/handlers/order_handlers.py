from sqlalchemy.orm import Session
from src.application.commands.order_commands import (
    CreateOrderCommand, UpdateOrderCommand, CancelOrderCommand,
    AddOrderItemCommand, UpdateOrderItemCommand, RemoveOrderItemCommand
)
from src.application.queries.order_queries import OrderDTO, GetOrderQuery, GetOrdersQuery, GetUserOrdersQuery
from src.infrastructure.repositories.order_repository import OrderRepository
from src.domain.models.order import Order, OrderItem
from typing import List
from decimal import Decimal


class CreateOrderHandler:
    def __init__(self, db: Session):
        self.order_repository = OrderRepository(db)

    def handle(self, command: CreateOrderCommand) -> OrderDTO:
        # Calculate totals
        subtotal = sum(item['quantity'] * item['unit_price'] for item in command.items)
        tax_amount = subtotal * Decimal('0.08')  # 8% tax
        shipping_cost = Decimal('10.00')  # Fixed shipping cost
        total_amount = subtotal + tax_amount + shipping_cost

        order_data = {
            'user_id': command.user_id,
            'payment_method': command.payment_method,
            'subtotal': float(subtotal),
            'tax_amount': float(tax_amount),
            'shipping_cost': float(shipping_cost),
            'total_amount': float(total_amount),
            'shipping_address': command.shipping_address,
            'billing_address': command.billing_address,
            'notes': command.notes
        }

        order = self.order_repository.create(order_data)

        # Add order items
        for item in command.items:
            item_data = {
                'product_id': item['product_id'],
                'quantity': item['quantity'],
                'unit_price': item['unit_price'],
                'total_price': float(item['quantity'] * item['unit_price'])
            }
            self.order_repository.add_item(order.id, item_data)

        # Refresh order with items
        order = self.order_repository.get_by_id(order.id)
        return OrderDTO.model_validate(order)


class UpdateOrderHandler:
    def __init__(self, db: Session):
        self.order_repository = OrderRepository(db)

    def handle(self, order_id: int, command: UpdateOrderCommand) -> OrderDTO:
        update_data = command.model_dump(exclude_unset=True)
        order = self.order_repository.update(order_id, update_data)
        if not order:
            raise ValueError(f"Order with id {order_id} not found")
        return OrderDTO.model_validate(order)


class CancelOrderHandler:
    def __init__(self, db: Session):
        self.order_repository = OrderRepository(db)

    def handle(self, command: CancelOrderCommand) -> OrderDTO:
        order = self.order_repository.update_status(command.order_id, 'cancelled')
        if not order:
            raise ValueError(f"Order with id {command.order_id} not found")
        return OrderDTO.model_validate(order)


class AddOrderItemHandler:
    def __init__(self, db: Session):
        self.order_repository = OrderRepository(db)

    def handle(self, command: AddOrderItemCommand) -> OrderItem:
        item_data = {
            'product_id': command.product_id,
            'quantity': command.quantity,
            'unit_price': command.unit_price,
            'total_price': float(command.quantity * command.unit_price)
        }
        item = self.order_repository.add_item(command.order_id, item_data)
        return item


class UpdateOrderItemHandler:
    def __init__(self, db: Session):
        self.order_repository = OrderRepository(db)

    def handle(self, command: UpdateOrderItemCommand) -> OrderItem:
        update_data = command.model_dump(exclude_unset=True)
        item = self.order_repository.update_item(command.item_id, update_data)
        if not item:
            raise ValueError(f"Order item with id {command.item_id} not found")
        return item


class RemoveOrderItemHandler:
    def __init__(self, db: Session):
        self.order_repository = OrderRepository(db)

    def handle(self, command: RemoveOrderItemCommand) -> bool:
        success = self.order_repository.delete_item(command.item_id)
        if not success:
            raise ValueError(f"Order item with id {command.item_id} not found")
        return success


class GetOrderHandler:
    def __init__(self, db: Session):
        self.order_repository = OrderRepository(db)

    def handle(self, query: GetOrderQuery) -> OrderDTO:
        order = self.order_repository.get_by_id(query.order_id)
        if not order:
            raise ValueError(f"Order with id {query.order_id} not found")
        return OrderDTO.model_validate(order)


class GetOrdersHandler:
    def __init__(self, db: Session):
        self.order_repository = OrderRepository(db)

    def handle(self, query: GetOrdersQuery) -> List[OrderDTO]:
        orders = self.order_repository.get_all(
            skip=query.skip,
            limit=query.limit,
            status=query.status
        )
        return [OrderDTO.model_validate(order) for order in orders]


class GetUserOrdersHandler:
    def __init__(self, db: Session):
        self.order_repository = OrderRepository(db)

    def handle(self, query: GetUserOrdersQuery) -> List[OrderDTO]:
        orders = self.order_repository.get_by_user_id(
            query.user_id,
            skip=query.skip,
            limit=query.limit
        )
        return [OrderDTO.model_validate(order) for order in orders]