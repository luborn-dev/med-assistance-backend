from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.database import db
from app.routers import (
    patients_router,
    procedures_router,
    summarize_router,
    users_router,
)

origins = ["*"]


async def lifespan(app: FastAPI):
    await db.connect()
    yield
    await db.close_connection()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(procedures_router.router, prefix="/api")
app.include_router(users_router.router, prefix="/api")
app.include_router(patients_router.router, prefix="/api")
app.include_router(summarize_router.router, prefix="/api")
