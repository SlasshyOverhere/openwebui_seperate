import socketio
import asyncio
from fastapi import FastAPI
from starlette.applications import Starlette

# Create a simple Socket.IO server
sio = socketio.AsyncServer(
    cors_allowed_origins=["http://localhost:6969", "http://127.0.0.1:6969"],
    async_mode="asgi",
    transports=["websocket", "polling"],
    allow_upgrades=True,
    always_connect=True
)

# Create the Socket.IO app
socket_app = socketio.ASGIApp(sio)

# Socket event handlers
@sio.event
async def connect(sid, environ, auth):
    # Join client to default room for chat events
    await sio.enter_room(sid, "default")
    await sio.enter_room(sid, "chat")
    await sio.emit("connected", {"data": "Connected to server"}, room=sid)

@sio.event
async def disconnect(sid):
    # Client disconnected
    pass

@sio.event
async def join(sid, data):
    # Client joined room
    pass

@sio.event
async def leave(sid, data):
    # Client left room
    pass

@sio.event
async def chat_message(sid, data):
    # Chat message received
    pass

@sio.event
async def user_join(sid, data):
    # User join event
    pass

@sio.event
async def chat_events(sid, data):
    # Chat events received
    pass

# Function to emit chat events (called from main.py)
async def emit_chat_event(event_type, data, room="chat"):
    """Emit chat events to connected clients"""
    try:
        await sio.emit(event_type, data, room=room)
    except Exception as e:
        pass

# Function to emit chat-events (for compatibility with existing code)
async def emit_chat_events(data, room="chat"):
    """Emit chat-events to connected clients"""
    try:
        await sio.emit("chat-events", data, room=room)
    except Exception as e:
        pass

# Function to get connected clients
async def get_connected_clients():
    """Get list of connected client IDs"""
    return list(sio.rooms.keys())

# Export the socket app for mounting in main.py
__all__ = ["socket_app", "emit_chat_event", "emit_chat_events", "get_connected_clients"]
