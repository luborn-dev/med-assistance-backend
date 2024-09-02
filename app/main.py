from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.database import db
from app.routers import patients, procedure, summarize, users

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

app.include_router(procedure.router)
app.include_router(users.router)
app.include_router(patients.router)
app.include_router(summarize.router)
