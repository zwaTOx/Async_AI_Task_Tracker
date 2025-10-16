from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.database import init_db
from src.user.routes import user_router
from src.project.routes import project_router
from src.category.routes import category_router
from src.user_project_association.routes import user_project_as_router
from src.code.routes import code_router
from src.attachment.routes import attach_router
from src.task.routes import task_router
from src.subtask.routes import subtask_router
from src.notification.routes import notification_router

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

@app.get('/')
async def ping():
    return {'msg': 'pong'}

app.include_router(
    user_router, prefix='/api', tags=['User']
)
app.include_router(
    code_router, prefix="/api/restore", tags=["Codes"]
)
app.include_router(
    category_router, prefix="/api/categories", tags = ['Category']
)
app.include_router(
    project_router, prefix='/api/projects', tags=['Project']
)

app.include_router(
    user_project_as_router, prefix='/api/projects', tags=['User in Project']
)
app.include_router(
    attach_router, prefix="/api", tags=["Attachment"]
)
app.include_router(
    task_router, prefix="/api/projects",  tags=["Task"]
)
app.include_router(
    subtask_router, prefix="/api", tags=["Subtask"]
)
app.include_router(
    notification_router, prefix="/api/notifications", tags=["Notification"]
)