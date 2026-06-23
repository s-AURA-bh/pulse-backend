from pydantic import BaseModel


class GoalCreate(BaseModel):
    title: str
    description: str | None = None


class GoalUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None


class GoalResponse(BaseModel):
    id: int
    title: str
    description: str | None
    completed: bool

    class Config:
        from_attributes = True
