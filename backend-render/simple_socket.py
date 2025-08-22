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
    print(f"Client connected: {sid}")
    # Join client to default room for chat events
    await sio.enter_room(sid, "default")
    await sio.enter_room(sid, "chat")
    await sio.emit("connected", {"data": "Connected to server"}, room=sid)

@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")

@sio.event
async def join(sid, data):
    print(f"Client {sid} joined room: {data}")
    await sio.enter_room(sid, data)

@sio.event
async def leave(sid, data):
    print(f"Client {sid} left room: {data}")
    await sio.leave_room(sid, data)

@sio.event
async def chat_message(sid, data):
    print(f"Chat message from {sid}: {data}")
    # Broadcast to all clients in the same room
    room = data.get("room", "default")
    await sio.emit("chat_message", data, room=room, skip_sid=sid)

@sio.event
async def user_join(sid, data):
    print(f"User join event from {sid}: {data}")
    # Handle user authentication and room joining
    if data.get("auth", {}).get("token"):
        # Join user to chat room for receiving events
        await sio.enter_room(sid, "chat")
        await sio.emit("user_joined", {"user": sid, "data": data}, room="chat")
        print(f"User {sid} joined chat room")

@sio.event
async def chat_events(sid, data):
    print(f"Chat events from {sid}: {data}")
    # Handle chat events from frontend
    await sio.emit("chat-events", data, room="chat", skip_sid=sid)

# Function to emit chat events (called from main.py)
async def emit_chat_event(event_type, data, room="chat"):
    """Emit chat events to connected clients"""
    print(f"Emitting {event_type} to room {room}: {data}")
    await sio.emit(event_type, data, room=room)
    print(f"Emitted {event_type} successfully")

# Function to emit chat-events (for compatibility with existing code)
async def emit_chat_events(data, room="chat"):
    """Emit chat-events to connected clients"""
    print(f"Emitting chat-events to room {room}: {data}")
    await sio.emit("chat-events", data, room=room)
    print(f"Emitted chat-events successfully")

# Function to get connected clients
async def get_connected_clients():
    """Get list of connected client IDs"""
    return list(sio.rooms.keys())

# Export the socket app for mounting in main.py
__all__ = ["socket_app", "emit_chat_event", "emit_chat_events", "get_connected_clients"]
