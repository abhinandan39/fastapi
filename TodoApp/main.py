from typing import Annotated

from fastapi import FastAPI
from .database import engine
from .models import Base
from .routers import auth, todos, admin, users
app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)

@app.get("/healthy")
async def health_check():
    return {
        'status': 'healthy'
    }