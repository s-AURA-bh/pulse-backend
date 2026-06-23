from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserLogin, Token
from app.services.auth import AuthService
from app.core.security import hash_password
from app.models.user import User

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/register")
async def register(
    user: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    existing_user = await UserRepository.get_by_email(
        db,
        user.email,
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists",
        )

    new_user = User(
        email=user.email,
        password_hash=hash_password(user.password),
    )

    created_user = await UserRepository.create(
        db,
        new_user,
    )

    return {
        "id": created_user.id,
        "email": created_user.email,
    }


@router.post(
    "/login",
    response_model=Token,
)
async def login(
    payload: UserLogin,
    db: AsyncSession = Depends(get_db),
):
    token = await AuthService.login(
        db,
        payload.email,
        payload.password,
    )

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
        )

    return {
        "access_token": token,
        "token_type": "bearer",
    }
