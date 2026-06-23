from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task


class DashboardRepository:
    @staticmethod
    async def get_stats(
        db: AsyncSession,
        user_id: int,
    ):
        total_result = await db.execute(
            select(func.count(Task.id)).where(
                Task.user_id == user_id
            )
        )

        completed_result = await db.execute(
            select(func.count(Task.id)).where(
                Task.user_id == user_id,
                Task.completed == True,
            )
        )

        total_tasks = total_result.scalar() or 0
        completed_tasks = completed_result.scalar() or 0

        pending_tasks = (
            total_tasks - completed_tasks
        )

        completion_rate = 0.0

        if total_tasks > 0:
            completion_rate = round(
                (completed_tasks / total_tasks) * 100,
                2,
            )

        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,
            "completion_rate": completion_rate,
        }
