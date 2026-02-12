from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from config import settings
from database import engine, Base
from routers import auth, files, notes, calendar, ai_assistant

app = FastAPI(
    title="Sh7omyLab API",
    description="Personal cloud portal with storage, notes, calendar, and AI assistance",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(files.router, prefix="/api/v1/files", tags=["files"])
app.include_router(notes.router, prefix="/api/v1/notes", tags=["notes"])
app.include_router(calendar.router, prefix="/api/v1/calendar", tags=["calendar"])
app.include_router(ai_assistant.router, prefix="/api/v1/ai", tags=["ai"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Sh7omyLab API"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Sh7omyLab API"}

if __name__ == "__main__":
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)