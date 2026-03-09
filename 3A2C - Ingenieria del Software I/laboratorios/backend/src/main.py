import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from db import Base, engine, SessionLocal
from contextlib import asynccontextmanager
from routers import game_routers

from realtime.sockets import sio_app
from realtime import sio_handler  
from services.action_timer_service import ActionTimerService


timer_service = ActionTimerService(SessionLocal)


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    
    await timer_service.start()
    
    yield
    
    await timer_service.stop()


app = FastAPI(lifespan=lifespan)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(game_routers.games_router)

# Mount the Socket.IO app
app.mount("/", app=sio_app)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=8000)
