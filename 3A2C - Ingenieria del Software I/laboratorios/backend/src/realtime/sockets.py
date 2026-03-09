import socketio

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins=[])

sio_app = socketio.ASGIApp(socketio_server=sio)
