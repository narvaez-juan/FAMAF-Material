"""Application main module."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from agenda.models.db import Base, engine
from agenda.tags.constants import DEFAULT_TAGS
from agenda.tags.utils import populate_tags
from agenda.websockets import websocket_router
from constants import WS_TEST_HTML
from api import api_router
from constants import DB_PROVIDER, PROJECT_DESCRIPTION, PROJECT_NAME
from settings import settings
from version import __API__VERSION

app = FastAPI(
    title=PROJECT_NAME,
    description=PROJECT_DESCRIPTION,
    version=__API__VERSION,
    root_path=settings.ROOT_PATH,
    debug=settings.DEBUG_MODE,
)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/version")
async def version():
    """
    gets api version

    Returns
    -------
    Dict
        returns api version
    """
    return {"version": __API__VERSION}


# Including routers
app.include_router(api_router)
app.include_router(websocket_router)


@app.get("/ws_test")
async def websocket_test():
    return HTMLResponse(WS_TEST_HTML)


# Connecting to DB and creating tables
Base.metadata.create_all(engine)
populate_tags(tags=DEFAULT_TAGS)
