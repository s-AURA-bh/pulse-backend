from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.get("/me")
async def me(
    current_user: User = Depends(get_current_user),
):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "created_at": current_user.created_at,
    }
