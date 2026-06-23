from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task


class TaskRepository:
    @staticmethod
    async def create(
        db: AsyncSession,
        task: Task,
    ):
        db.add(task)

        await db.commit()
        await db.refresh(task)

        return task

    @staticmethod
    async def get_all_by_user(
        db: AsyncSession,
        user_id: int,
    ):
        result = await db.execute(
            select(Task).where(
                Task.user_id == user_id
            )
        )

        return result.scalars().all()

    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        task_id: int,
    ):
        result = await db.execute(
            select(Task).where(
                Task.id == task_id
            )
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def update(
        db: AsyncSession,
        task: Task,
    ):
        await db.commit()
        await db.refresh(task)

        return task
    @staticmethod
    async def delete(
        db: AsyncSession,
        task: Task,
    ):
        await db.delete(task)
        await db.commit()
