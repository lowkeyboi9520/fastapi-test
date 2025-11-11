from sqlalchemy.orm import Session
from src.application.commands.user_commands import CreateUserCommand, UpdateUserCommand, DeleteUserCommand
from src.application.queries.user_queries import UserDTO, GetUserQuery, GetUsersQuery
from src.infrastructure.repositories.user_repository import UserRepository
from src.domain.models.user import User
from src.core.auth import get_password_hash
from typing import List
from datetime import datetime


class CreateUserHandler:
    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)

    def handle(self, command: CreateUserCommand) -> UserDTO:
        # Hash the password
        hashed_password = get_password_hash(command.password)
        user_data = command.model_copy()
        user_data.password = hashed_password
        user_dict = user_data.model_dump()
        user = self.user_repository.create(user_dict)
        return UserDTO.model_validate(user)


class UpdateUserHandler:
    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)

    def handle(self, user_id: int, command: UpdateUserCommand) -> UserDTO:
        update_data = command.model_dump(exclude_unset=True)
        user = self.user_repository.update(user_id, update_data)
        if not user:
            raise ValueError(f"User with id {user_id} not found")
        return UserDTO.model_validate(user)


class DeleteUserHandler:
    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)

    def handle(self, command: DeleteUserCommand) -> bool:
        success = self.user_repository.delete(command.user_id)
        if not success:
            raise ValueError(f"User with id {command.user_id} not found")
        return success


class GetUserHandler:
    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)

    def handle(self, query: GetUserQuery) -> UserDTO:
        user = self.user_repository.get_by_id(query.user_id)
        if not user:
            raise ValueError(f"User with id {query.user_id} not found")
        return UserDTO.model_validate(user)


class GetUsersHandler:
    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)

    def handle(self, query: GetUsersQuery) -> List[UserDTO]:
        users = self.user_repository.get_all(
            skip=query.skip,
            limit=query.limit,
            role=query.role,
            is_active=query.is_active
        )
        return [UserDTO.model_validate(user) for user in users]