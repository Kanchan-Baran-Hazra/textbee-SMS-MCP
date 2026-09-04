from fastapi import FastAPI
from .users.routes import user_router
from .db.main import Base, engine





app = FastAPI(
    title="My FastAPI Application",
    version="1.0.0",
    description="This is a sample FastAPI application with JWT authentication.",
)

# Create database tables
Base.metadata.create_all(
    bind=engine
)

app.include_router(user_router, prefix="/users", tags=["users"])



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9000)