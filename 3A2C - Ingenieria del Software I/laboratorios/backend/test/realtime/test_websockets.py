import asyncio
import socketio
import uvicorn
import pytest
import pytest_asyncio

# ---- ASGI test server ----
srv_sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
srv_app = socketio.ASGIApp(srv_sio, socketio_path="socket.io")


@srv_sio.event
async def connect(sid, environ):
    pass


@srv_sio.event
async def disconnect(sid):
    pass


# ---- test client ----
cli_sio = socketio.AsyncClient()
connected = False
disconnected = False


@cli_sio.event
async def connect():
    global connected
    connected = True


@cli_sio.event
async def disconnect():
    global disconnected
    disconnected = True


@pytest_asyncio.fixture
async def running_server(unused_tcp_port):
    port = unused_tcp_port
    config = uvicorn.Config(
        srv_app,
        host="127.0.0.1",
        port=port,
        log_level="warning",
        loop="asyncio",
    )
    server = uvicorn.Server(config)

    task = asyncio.create_task(server.serve())
    # Wait till start
    while not server.started:
        await asyncio.sleep(0.01)

    try:
        yield f"http://127.0.0.1:{port}"
    finally:
        server.should_exit = True
        await task  # clean shutdown


@pytest.mark.asyncio
async def test_socketio_connect_disconnect(running_server):
    global connected, disconnected
    connected = False
    disconnected = False

    await cli_sio.connect(
        running_server,
        socketio_path="socket.io",
        transports=["websocket"],
        wait=True,
        wait_timeout=2,
    )

    await asyncio.sleep(0.05)
    assert connected is True

    await cli_sio.disconnect()
    await asyncio.sleep(0.05)
    assert disconnected is True
