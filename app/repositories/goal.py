from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.goal import Goal


class GoalRepository:
    @staticmethod
    async def create(
        db: AsyncSession,
        goal: Goal,
    ):
        db.add(goal)

        await db.commit()
        await db.refresh(goal)

        return goal

    @staticmethod
    async def get_all_by_user(
        db: AsyncSession,
        user_id: int,
    ):
        result = await db.execute(
            select(Goal).where(
                Goal.user_id == user_id
            )
        )

        return result.scalars().all()

    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        goal_id: int,
    ):
        result = await db.execute(
            select(Goal).where(
                Goal.id == goal_id
            )
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def update(
        db: AsyncSession,
        goal: Goal,
    ):
        await db.commit()
        await db.refresh(goal)

        return goal

    @staticmethod
    async def delete(
        db: AsyncSession,
        goal: Goal,
    ):
        await db.delete(goal)
        await db.commit()
