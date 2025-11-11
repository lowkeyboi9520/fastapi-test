from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from src.infrastructure.database import get_db
from src.api.auth_routers import get_current_active_user
from src.application.queries.user_queries import UserDTO
from src.application.commands.user_commands import (
    CreateUserCommand, UpdateUserCommand, DeleteUserCommand
)
from src.application.queries.user_queries import (
    GetUserQuery, GetUsersQuery, UserDTO
)
from src.application.handlers.user_handlers import (
    CreateUserHandler, UpdateUserHandler, DeleteUserHandler,
    GetUserHandler, GetUsersHandler
)

router = APIRouter()


@router.post("/users", response_model=UserDTO, status_code=201)
async def create_user(
    command: CreateUserCommand,
    db: Session = Depends(get_db)
):
    handler = CreateUserHandler(db)
    return handler.handle(command)


@router.get("/users/{user_id}", response_model=UserDTO)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    handler = GetUserHandler(db)
    query = GetUserQuery(user_id=user_id)
    try:
        return handler.handle(query)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/users", response_model=list[UserDTO])
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    role: str = Query(None, pattern="^(customer|admin|moderator)$"),
    is_active: bool = Query(True),
    db: Session = Depends(get_db)
):
    handler = GetUsersHandler(db)
    query = GetUsersQuery(
        skip=skip,
        limit=limit,
        role=role,
        is_active=is_active
    )
    return handler.handle(query)


@router.put("/users/{user_id}", response_model=UserDTO)
async def update_user(
    user_id: int,
    command: UpdateUserCommand,
    current_user: UserDTO = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    handler = UpdateUserHandler(db)
    try:
        return handler.handle(user_id, command)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    current_user: UserDTO = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    handler = DeleteUserHandler(db)
    command = DeleteUserCommand(user_id=user_id)
    try:
        handler.handle(command)
        return {"message": "User deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/users/me", response_model=UserDTO)
async def get_current_user_info(current_user: UserDTO = Depends(get_current_active_user)):
    return current_user