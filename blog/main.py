from fastapi import FastAPI
from . import models
from .database import engine
from .routers import blog, user, login
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

app = FastAPI(
    title="My FastAPI",
    description="Blog Page",
    version="0.1.0",
    default_response_class=ORJSONResponse
)

origins = [
    "https://www.PsiBlog.com",
    "http://www.PsiBlog.com",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.ModelDB.metadata.create_all(engine)

app.include_router(login.router)
app.include_router(user.router)
app.include_router(blog.router)

