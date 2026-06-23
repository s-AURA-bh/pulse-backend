from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.database.session import get_db
from app.models.note import Note
from app.models.user import User
from app.repositories.note import NoteRepository
from app.schemas.note import (
    NoteCreate,
    NoteUpdate,
    NoteResponse,
)

router = APIRouter(
    prefix="/notes",
    tags=["notes"],
)


@router.post(
    "",
    response_model=NoteResponse,
)
async def create_note(
    payload: NoteCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    note = Note(
        title=payload.title,
        content=payload.content,
        user_id=current_user.id,
    )

    return await NoteRepository.create(
        db,
        note,
    )


@router.get(
    "",
    response_model=list[NoteResponse],
)
async def list_notes(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await NoteRepository.get_all_by_user(
        db,
        current_user.id,
    )


@router.patch(
    "/{note_id}",
    response_model=NoteResponse,
)
async def update_note(
    note_id: int,
    payload: NoteUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    note = await NoteRepository.get_by_id(
        db,
        note_id,
    )

    if not note:
        raise HTTPException(
            status_code=404,
            detail="Note not found",
        )

    if note.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Forbidden",
        )

    if payload.title is not None:
        note.title = payload.title

    if payload.content is not None:
        note.content = payload.content

    return await NoteRepository.update(
        db,
        note,
    )


@router.delete(
    "/{note_id}",
)
async def delete_note(
    note_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    note = await NoteRepository.get_by_id(
        db,
        note_id,
    )

    if not note:
        raise HTTPException(
            status_code=404,
            detail="Note not found",
        )

    if note.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Forbidden",
        )

    await NoteRepository.delete(
        db,
        note,
    )

    return {
        "message": "Note deleted",
    }
