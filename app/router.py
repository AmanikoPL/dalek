from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.auth import router as auth_router
from app.api.parsers import router as parsers_router
from app.api.game_status import router as game_status_router

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(parsers_router, prefix="/parse", tags=["Parsers"])
app.include_router(game_status_router)
