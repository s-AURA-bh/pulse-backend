from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.database.session import get_db
from app.models.goal import Goal
from app.models.user import User
from app.repositories.goal import GoalRepository
from app.schemas.goal import (
    GoalCreate,
    GoalUpdate,
    GoalResponse,
)

router = APIRouter(
    prefix="/goals",
    tags=["goals"],
)


@router.post(
    "",
    response_model=GoalResponse,
)
async def create_goal(
    payload: GoalCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    goal = Goal(
        title=payload.title,
        description=payload.description,
        user_id=current_user.id,
    )

    return await GoalRepository.create(
        db,
        goal,
    )


@router.get(
    "",
    response_model=list[GoalResponse],
)
async def list_goals(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await GoalRepository.get_all_by_user(
        db,
        current_user.id,
    )


@router.patch(
    "/{goal_id}",
    response_model=GoalResponse,
)
async def update_goal(
    goal_id: int,
    payload: GoalUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    goal = await GoalRepository.get_by_id(
        db,
        goal_id,
    )

    if not goal:
        raise HTTPException(
            status_code=404,
            detail="Goal not found",
        )

    if goal.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Forbidden",
        )

    if payload.title is not None:
        goal.title = payload.title

    if payload.description is not None:
        goal.description = payload.description

    if payload.completed is not None:
        goal.completed = payload.completed

    return await GoalRepository.update(
        db,
        goal,
    )


@router.delete(
    "/{goal_id}",
)
async def delete_goal(
    goal_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    goal = await GoalRepository.get_by_id(
        db,
        goal_id,
    )

    if not goal:
        raise HTTPException(
            status_code=404,
            detail="Goal not found",
        )

    if goal.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Forbidden",
        )

    await GoalRepository.delete(
        db,
        goal,
    )

    return {
        "message": "Goal deleted",
    }
