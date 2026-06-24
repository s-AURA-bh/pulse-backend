from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.tasks import router as tasks_router
from app.api.dashboard import router as dashboard_router
from app.api.goals import router as goals_router
from app.api.notes import router as notes_router

app = FastAPI(title="Pulse API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "https://pulse-frontend-967coputz-saurabh4934.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(tasks_router)
app.include_router(dashboard_router)
app.include_router(goals_router)
app.include_router(notes_router)

@app.get("/health")
async def health():
    return {"status": "ok"}
