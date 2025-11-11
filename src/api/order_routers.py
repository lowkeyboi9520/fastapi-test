from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from src.infrastructure.database import get_db
from src.application.commands.order_commands import (
    CreateOrderCommand, UpdateOrderCommand, CancelOrderCommand,
    AddOrderItemCommand, UpdateOrderItemCommand, RemoveOrderItemCommand
)
from src.application.queries.order_queries import (
    GetOrderQuery, GetOrdersQuery, GetUserOrdersQuery, OrderDTO
)
from src.application.handlers.order_handlers import (
    CreateOrderHandler, UpdateOrderHandler, CancelOrderHandler,
    GetOrderHandler, GetOrdersHandler, GetUserOrdersHandler
)

router = APIRouter()


@router.post("/orders", response_model=OrderDTO, status_code=201)
async def create_order(
    command: CreateOrderCommand,
    db: Session = Depends(get_db)
):
    handler = CreateOrderHandler(db)
    return handler.handle(command)


@router.get("/orders/{order_id}", response_model=OrderDTO)
async def get_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    handler = GetOrderHandler(db)
    query = GetOrderQuery(order_id=order_id)
    try:
        return handler.handle(query)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/orders", response_model=list[OrderDTO])
async def get_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status: str = Query(None, pattern="^(pending|confirmed|processing|shipped|delivered|cancelled)$"),
    db: Session = Depends(get_db)
):
    handler = GetOrdersHandler(db)
    query = GetOrdersQuery(
        skip=skip,
        limit=limit,
        status=status
    )
    return handler.handle(query)


@router.get("/users/{user_id}/orders", response_model=list[OrderDTO])
async def get_user_orders(
    user_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    handler = GetUserOrdersHandler(db)
    query = GetUserOrdersQuery(
        user_id=user_id,
        skip=skip,
        limit=limit
    )
    return handler.handle(query)


@router.put("/orders/{order_id}", response_model=OrderDTO)
async def update_order(
    order_id: int,
    command: UpdateOrderCommand,
    db: Session = Depends(get_db)
):
    handler = UpdateOrderHandler(db)
    try:
        return handler.handle(order_id, command)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/orders/{order_id}/cancel", response_model=OrderDTO)
async def cancel_order(
    order_id: int,
    reason: str = None,
    db: Session = Depends(get_db)
):
    from src.application.commands.order_commands import CancelOrderCommand
    handler = CancelOrderHandler(db)
    command = CancelOrderCommand(order_id=order_id, reason=reason)
    try:
        return handler.handle(command)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/orders/{order_id}/items", response_model=OrderDTO)
async def add_order_item(
    order_id: int,
    command: AddOrderItemCommand,
    db: Session = Depends(get_db)
):
    # Override order_id from the URL
    command.order_id = order_id
    from src.application.handlers.order_handlers import AddOrderItemHandler
    handler = AddOrderItemHandler(db)
    item = handler.handle(command)
    return item


@router.put("/orders/items/{item_id}", response_model=OrderDTO)
async def update_order_item(
    item_id: int,
    command: UpdateOrderItemCommand,
    db: Session = Depends(get_db)
):
    handler = UpdateOrderItemHandler(db)
    try:
        return handler.handle(command)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/orders/items/{item_id}")
async def remove_order_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    handler = RemoveOrderItemHandler(db)
    command = RemoveOrderItemCommand(item_id=item_id)
    try:
        handler.handle(command)
        return {"message": "Order item removed successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))