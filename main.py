from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict
from datetime import datetime, timedelta
from core_logic.leaky_bucket import LeakyBucket
from core_logic.database import Database
import os

app = FastAPI()

# Mount uploads directory for serving files
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Database instance
db = Database("chat_history.db")

# Active connections
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.user_buckets: Dict[str, LeakyBucket] = {}

    async def connect(self, username: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[username] = websocket
        self.user_buckets[username] = LeakyBucket(capacity=5, leak_rate=1.0)
        await self.broadcast_user_list()

    def disconnect(self, username: str):
        if username in self.active_connections:
            del self.active_connections[username]
        if username in self.user_buckets:
            del self.user_buckets[username]

    async def send_personal_message(self, message: dict, username: str):
        if username in self.active_connections:
            await self.active_connections[username].send_json(message)

    async def broadcast(self, message: dict, exclude: str = None):
        for username, connection in self.active_connections.items():
            if username != exclude:
                await connection.send_json(message)

    async def broadcast_user_list(self):
        users = list(self.active_connections.keys())
        connections = list(self.active_connections.values())
        for connection in connections:
            try:
                await connection.send_json({
                    "type": "user_list",
                    "users": users
                })
            except:
                pass

    def check_rate_limit(self, username: str) -> tuple:
        if username not in self.user_buckets:
            return True, ""
        
        bucket = self.user_buckets[username]
        if bucket.add_message():
            return True, ""
        else:
            wait_time = int((bucket._current_level - bucket.capacity) / bucket.leak_rate) + 1
            return False, f"Slow down! Please wait {wait_time} seconds before sending another message."


manager = ConnectionManager()


# Models
class UserRegister(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


# API Endpoints
@app.post("/api/register")
async def register(user: UserRegister):
    """Register a new user."""
    if len(user.username) < 2 or len(user.username) > 20:
        raise HTTPException(status_code=400, detail="Username must be between 2 and 20 characters")
    
    if len(user.password) < 4:
        raise HTTPException(status_code=400, detail="Password must be at least 4 characters")
    
    success = db.create_user(user.username, user.password)
    if success:
        return {"message": "User registered successfully"}
    else:
        raise HTTPException(status_code=400, detail="Username already exists")


@app.post("/api/login")
async def login(user: UserLogin):
    """Login user."""
    if db.verify_user(user.username, user.password):
        return {"message": "Login successful", "username": user.username}
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")


@app.get("/", response_class=HTMLResponse)
async def get_chat_page():
    """Serve the chat HTML page."""
    with open("templates/chat.html", "r", encoding="utf-8") as f:
        return f.read()


@app.get("/admin", response_class=HTMLResponse)
async def get_admin_page():
    """Serve the admin dashboard HTML page."""
    with open("templates/admin.html", "r", encoding="utf-8") as f:
        return f.read()


# Admin API - Get Statistics
@app.get("/api/admin/stats")
async def get_admin_stats():
    """Get system statistics for admin dashboard."""
    total_users = db.get_total_users()
    online_users = len(manager.active_connections)
    total_messages = db.get_total_messages()
    messages_today = db.get_messages_today()
    group_messages = db.get_group_message_count()
    private_messages = total_messages - group_messages
    
    return {
        "total_users": total_users,
        "online_users": online_users,
        "total_messages": total_messages,
        "messages_today": messages_today,
        "group_messages": group_messages,
        "private_messages": private_messages
    }


# Admin API - Get All Users
@app.get("/api/admin/users")
async def get_all_users():
    """Get all registered users with their stats."""
    users = db.get_all_users_with_stats()
    
    # Add online status
    for user in users:
        user['is_online'] = user['username'] in manager.active_connections
    
    return users


# Admin API - Get All Messages
@app.get("/api/admin/messages")
async def get_all_messages():
    """Get all messages from the system."""
    return db.get_all_messages()


# Enhanced API Endpoints
@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload a file or image."""
    import os
    import uuid
    from pathlib import Path
    
    # Create uploads directory if it doesn't exist
    uploads_dir = Path("uploads")
    uploads_dir.mkdir(exist_ok=True)
    
    # Generate unique filename
    file_extension = Path(file.filename).suffix.lower()
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = uploads_dir / unique_filename
    
    # Save file
    try:
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
        
        # Determine file type
        if file.content_type and file.content_type.startswith("image/"):
            file_type = "image"
        elif file_extension in ['.pdf']:
            file_type = "pdf"
        elif file_extension in ['.doc', '.docx']:
            file_type = "document"
        elif file_extension in ['.xls', '.xlsx']:
            file_type = "spreadsheet"
        elif file_extension in ['.ppt', '.pptx']:
            file_type = "presentation"
        elif file_extension in ['.zip', '.rar', '.7z']:
            file_type = "archive"
        elif file_extension in ['.mp4', '.avi', '.mov']:
            file_type = "video"
        elif file_extension in ['.mp3', '.wav', '.ogg']:
            file_type = "audio"
        else:
            file_type = "file"
        
        return {
            "file_url": f"/uploads/{unique_filename}",
            "file_type": file_type,
            "filename": file.filename,
            "size": len(contents)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/search")
async def search_messages_api(q: str, username: str = None):
    """Search messages."""
    results = db.search_messages(q, username)
    return {"results": results}


@app.get("/api/user/{username}")
async def get_user_info_api(username: str):
    """Get user information."""
    user_info = db.get_user_info(username)
    if user_info:
        return user_info
    raise HTTPException(status_code=404, detail="User not found")


@app.get("/api/users/all")
async def get_all_users_api():
    """Get all registered users."""
    users = db.get_all_users()
    return {"users": users}
    user_info = db.get_user_info(username)
    if user_info:
        return user_info
    else:
        raise HTTPException(status_code=404, detail="User not found")


@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    """WebSocket connection for real-time chat."""
    
    # Verify user exists in database
    if not db.user_exists(username):
        await websocket.close(code=1008, reason="User not found")
        return
    
    await manager.connect(username, websocket)
    
    try:
        while True:
            data = await websocket.receive_json()
            message_type = data.get("type")

            if message_type == "get_history":
                # Get message history
                recipient = data.get("recipient", "GROUP")
                if recipient == "GROUP":
                    messages = db.get_group_messages_enhanced()
                else:
                    messages = db.get_private_messages_enhanced(username, recipient)
                
                await manager.send_personal_message({
                    "type": "history",
                    "messages": messages
                }, username)

            elif message_type == "typing":
                # Broadcast typing indicator
                recipient = data.get("recipient", "GROUP")
                if recipient == "GROUP":
                    await manager.broadcast({
                        "type": "user_typing",
                        "username": username,
                        "recipient": "GROUP"
                    }, exclude=username)
                else:
                    # Send to the other person that 'username' is typing to them
                    await manager.send_personal_message({
                        "type": "user_typing",
                        "username": username,
                        "recipient": username  # This indicates who is typing (the sender)
                    }, recipient)

            elif message_type == "stop_typing":
                # Broadcast stop typing
                recipient = data.get("recipient", "GROUP")
                if recipient == "GROUP":
                    await manager.broadcast({
                        "type": "user_stop_typing",
                        "username": username,
                        "recipient": "GROUP"
                    }, exclude=username)
                else:
                    await manager.send_personal_message({
                        "type": "user_stop_typing",
                        "username": username,
                        "recipient": username  # This indicates who stopped typing (the sender)
                    }, recipient)

            elif message_type == "react":
                # Add reaction to message
                message_id = data.get("message_id")
                emoji = data.get("emoji")
                if message_id and emoji:
                    db.add_reaction(message_id, username, emoji)
                    # Broadcast reaction update
                    await manager.broadcast({
                        "type": "reaction_update",
                        "message_id": message_id,
                        "emoji": emoji,
                        "username": username
                    })

            elif message_type == "edit":
                # Edit message
                message_id = data.get("message_id")
                new_text = data.get("new_text", "").strip()
                if message_id and new_text:
                    db.update_message(message_id, new_text)
                    await manager.broadcast({
                        "type": "message_edited",
                        "message_id": message_id,
                        "new_text": new_text,
                        "editor": username
                    })

            elif message_type == "delete":
                # Delete message
                message_id = data.get("message_id")
                if message_id:
                    db.delete_message(message_id)
                    await manager.broadcast({
                        "type": "message_deleted",
                        "message_id": message_id
                    })

            elif message_type == "search":
                # Search messages
                query = data.get("query", "").strip()
                if query:
                    results = db.search_messages(query, username)
                    await manager.send_personal_message({
                        "type": "search_results",
                        "results": results
                    }, username)

            elif message_type == "status_change":
                # Update user status
                status = data.get("status", "online")
                status_message = data.get("status_message", "")
                db.update_user_status(username, status, status_message)
                await manager.broadcast({
                    "type": "user_status_changed",
                    "username": username,
                    "status": status,
                    "status_message": status_message
                })

            elif message_type == "message":
                # Check rate limit
                can_send, warning = manager.check_rate_limit(username)
                
                if not can_send:
                    await manager.send_personal_message({
                        "type": "warning",
                        "message": warning
                    }, username)
                    continue

                # Process message
                message_text = data.get("message", "").strip()
                recipient = data.get("recipient", "GROUP")
                reply_to = data.get("reply_to")
                file_url = data.get("file_url")
                file_type = data.get("file_type")

                if not message_text and not file_url:
                    continue

                # Save message to database and get ID
                timestamp = datetime.now().isoformat()
                message_id = db.save_message_with_id(username, recipient, message_text, timestamp, reply_to, file_url, file_type)

                # Prepare message payload
                message_payload = {
                    "type": "message",
                    "id": message_id,
                    "sender": username,
                    "message": message_text,
                    "timestamp": timestamp,
                    "recipient": recipient,
                    "reply_to": reply_to,
                    "file_url": file_url,
                    "file_type": file_type,
                    "edited": False,
                    "reactions": []
                }

                # Send to appropriate recipients
                if recipient == "GROUP":
                    # Broadcast to all users
                    await manager.broadcast(message_payload)
                else:
                    # Send to specific user and sender
                    await manager.send_personal_message(message_payload, recipient)
                    await manager.send_personal_message(message_payload, username)

    except WebSocketDisconnect:
        manager.disconnect(username)
        await manager.broadcast_user_list()
    except Exception as e:
        print(f"Error: {e}")
        manager.disconnect(username)


if __name__ == "__main__":
    import uvicorn
    import socket
    
    # Get local IP address
    def get_local_ip():
        try:
            # Connect to an external server to get the local IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except:
            return "Unable to detect"
    
    local_ip = get_local_ip()
    port = 8000
    
    # Print banner
    print("\n" + "="*70)
    print("🚀 ChatMK - Real-Time Chat Application")
    print("="*70)
    
    print("\n📍 ACCESS YOUR CHAT:")
    print("-" * 70)
    
    # Local access
    print(f"   🏠 Local (this device):     http://localhost:{port}")
    print(f"                               http://127.0.0.1:{port}")
    
    # Network access
    if local_ip != "Unable to detect":
        print(f"\n   📱 Network (same WiFi):     http://{local_ip}:{port}")
        print(f"      → Share this with devices on your network")
    
    # Internet sharing options
    print("\n" + "="*70)
    print("🌐 SHARE OVER THE INTERNET:")
    print("="*70)
    
    print("\n   Option 1: Serveo (Easiest - No Installation)")
    print("   ─────────────────────────────────────────────")
    print("   1. Open a NEW terminal/command prompt")
    print("   2. Run: ssh -R 80:localhost:8000 serveo.net")
    print("   3. Share the https://xxx.serveo.net URL it gives you")
    print("   ✅ No installation, no signup, instant HTTPS\n")
    
    print("   Option 2: Cloudflare Tunnel (Recommended)")
    print("   ─────────────────────────────────────────────")
    print("   1. Install: https://developers.cloudflare.com/cloudflare-one/")
    print("   2. Run: cloudflared tunnel --url http://localhost:8000")
    print("   3. Share the https://xxx.trycloudflare.com URL")
    print("   ✅ Free, stable, professional\n")
    
    print("   Option 3: ngrok")
    print("   ─────────────────────────────────────────────")
    print("   1. Download from: https://ngrok.com/download")
    print("   2. Sign up and get auth token")
    print("   3. Run: ngrok http 8000")
    print("   4. Share the https://xxx.ngrok-free.app URL")
    print("   ✅ Popular, feature-rich\n")
    
    print("="*70)
    print("📚 DOCUMENTATION:")
    print("   • Setup Guide: SETUP_GUIDE.md")
    print("   • Features: docs/FEATURES_SUMMARY.md")
    print("   • Full docs: docs/README.md")
    print("="*70)
    
    print("\n🔥 Starting server...")
    print("   Press CTRL+C to stop\n")
    
    # Run the server
    uvicorn.run(app, host="0.0.0.0", port=port)