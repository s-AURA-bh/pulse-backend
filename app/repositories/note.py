from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.note import Note


class NoteRepository:
    @staticmethod
    async def create(
        db: AsyncSession,
        note: Note,
    ):
        db.add(note)

        await db.commit()
        await db.refresh(note)

        return note

    @staticmethod
    async def get_all_by_user(
        db: AsyncSession,
        user_id: int,
    ):
        result = await db.execute(
            select(Note).where(
                Note.user_id == user_id
            )
        )

        return result.scalars().all()

    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        note_id: int,
    ):
        result = await db.execute(
            select(Note).where(
                Note.id == note_id
            )
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def update(
        db: AsyncSession,
        note: Note,
    ):
        await db.commit()
        await db.refresh(note)

        return note

    @staticmethod
    async def delete(
        db: AsyncSession,
        note: Note,
    ):
        await db.delete(note)
        await db.commit()
