from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from cubersio.routers import competition as competition_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(competition_router.router)
