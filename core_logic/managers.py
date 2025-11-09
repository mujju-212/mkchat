import datetime  # <--- THIS IS THE FIX
from fastapi import WebSocket
from typing import List, Dict, Set

# --- Manager for the /logs dashboard ---
class LogManager:
    """Manages active WebSocket connections for the log dashboard."""
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast_log(self, message: str):
        """Broadcasts a log message to all connected admins."""
        for connection in list(self.active_connections):
            try:
                await connection.send_text(message)
            except:
                self.disconnect(connection)

# --- Manager for the /chat app ---
class ConnectionManager:
    """Manages active chat WebSocket connections."""
    
    def __init__(self):
        # A simple mapping of WebSocket -> client_id (username)
        self.client_ids: Dict[WebSocket, str] = {}

    def get_online_users(self) -> List[str]:
        """Returns a list of all current usernames."""
        return list(self.client_ids.values())

    async def connect(self, websocket: WebSocket, client_id: str):
        """Accepts a new client connection."""
        await websocket.accept()
        self.client_ids[websocket] = client_id
        await self.broadcast_user_list()

    async def disconnect(self, websocket: WebSocket) -> str:
        """Removes a client connection and returns their ID."""
        client_id = self.client_ids.pop(websocket, "Someone")
        await self.broadcast_user_list()
        return client_id

    async def broadcast_user_list(self):
        """Broadcasts the current user list to ALL connected clients."""
        user_list = self.get_online_users()
        msg_data = {
            "type": "USER_LIST",
            "users": user_list
        }
        for connection in self.client_ids.keys():
            try:
                await connection.send_json(msg_data)
            except:
                # Disconnect will be handled by main loop
                pass

    async def send_personal_json(self, data: dict, websocket: WebSocket):
        """Sends a JSON message to a specific client only (Unicast)."""
        try:
            await websocket.send_json(data)
        except:
            pass # Disconnect will be handled by main loop

    async def broadcast_message(self, sender: str, recipient: str, message: str):
        """
        Broadcasts a chat message to the relevant clients.
        If recipient is 'GROUP', sends to all.
        If recipient is a username, sends only to that user and the sender.
        """
        msg_data = {
            "type": "MESSAGE",
            "sender": sender,
            "recipient": recipient,
            "message": message,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        if recipient == 'GROUP':
            # Broadcast to everyone
            for connection in self.client_ids.keys():
                try:
                    await connection.send_json(msg_data)
                except:
                    pass
        else:
            # It's a DM, send only to sender and recipient
            recipient_ws = self.get_websocket_by_username(recipient)
            sender_ws = self.get_websocket_by_username(sender)
            
            if recipient_ws:
                try:
                    await recipient_ws.send_json(msg_data)
                except:
                    pass
            if sender_ws:
                 try:
                    await sender_ws.send_json(msg_data)
                 except:
                    pass

    async def broadcast_system_message(self, message: str):
        """Broadcasts a system message to all connected clients."""
        msg_data = {
            "type": "SYSTEM",
            "message": message,
            "timestamp": datetime.datetime.now().isoformat()
        }
        for connection in self.client_ids.keys():
            try:
                await connection.send_json(msg_data)
            except:
                pass

    def get_websocket_by_username(self, username: str) -> WebSocket | None:
        """Finds a WebSocket connection for a given username."""
        for ws, client_id in self.client_ids.items():
            if client_id == username:
                return ws
        return None
