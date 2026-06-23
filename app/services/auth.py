from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)
from app.models.user import User
from app.repositories.user import UserRepository


class AuthService:

    @staticmethod
    async def register(
        db,
        email: str,
        password: str,
    ):
        existing_user = await UserRepository.get_by_email(
            db,
            email,
        )

        if existing_user:
            raise ValueError(
                "User already exists"
            )

        user = User(
            email=email,
            password_hash=hash_password(password),
        )

        return await UserRepository.create(
            db,
            user,
        )

    @staticmethod
    async def login(
        db,
        email: str,
        password: str,
    ):
        user = await UserRepository.get_by_email(
            db,
            email,
        )

        if not user:
            return None

        if not verify_password(
            password,
            user.password_hash,
        ):
            return None

        token = create_access_token(
            str(user.id)
        )

        return token
