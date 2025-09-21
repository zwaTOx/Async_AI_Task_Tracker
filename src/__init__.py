from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.database import init_db
from src.user.routes import user_router
from src.project.routes import project_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print('Server is starting')
    await init_db()
    yield
    print('Server is shutting down')

app = FastAPI(
    title='AI Task Traker',
    lifespan=lifespan
)

@app.get('/')
async def ping():
    return {'msg': 'pong'}

app.include_router(
    user_router, prefix='/api/users', tags=['User']
)
app.include_router(
    project_router, prefix='/api/projects', tags=['Project']
)