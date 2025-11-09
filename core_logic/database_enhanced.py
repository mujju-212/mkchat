# Enhanced database methods - append these to database.py

def update_user_status(self, username: str, status: str, status_message: str = ""):
    """Update user status."""
    conn = sqlite3.connect(self.db_path)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET status = ?, status_message = ? WHERE username = ?",
        (status, status_message, username)
    )
    conn.commit()
    conn.close()

def get_user_info(self, username: str) -> Dict:
    """Get user information."""
    conn = sqlite3.connect(self.db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT username, avatar_color, status, status_message FROM users WHERE username = ?",
        (username,)
    )
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {
            "username": result[0],
            "avatar_color": result[1],
            "status": result[2],
            "status_message": result[3]
        }
    return None

def update_message(self, message_id: int, new_text: str):
    """Edit a message."""
    conn = sqlite3.connect(self.db_path)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE messages SET message = ?, edited = 1 WHERE id = ?",
        (new_text, message_id)
    )
    conn.commit()
    conn.close()

def delete_message(self, message_id: int):
    """Delete a message (soft delete)."""
    conn = sqlite3.connect(self.db_path)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE messages SET deleted = 1 WHERE id = ?",
        (message_id,)
    )
    conn.commit()
    conn.close()

def add_reaction(self, message_id: int, username: str, emoji: str):
    """Add a reaction to a message."""
    try:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        timestamp = datetime.utcnow().isoformat()
        cursor.execute(
            "INSERT INTO reactions (message_id, username, emoji, timestamp) VALUES (?, ?, ?, ?)",
            (message_id, username, emoji, timestamp)
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        # Reaction already exists, remove it
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM reactions WHERE message_id = ? AND username = ? AND emoji = ?",
            (message_id, username, emoji)
        )
        conn.commit()
        conn.close()
        return False

def get_message_reactions(self, message_id: int) -> List[Dict]:
    """Get reactions for a message."""
    conn = sqlite3.connect(self.db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT emoji, username FROM reactions WHERE message_id = ?",
        (message_id,)
    )
    reactions = []
    for row in cursor.fetchall():
        reactions.append({
            "emoji": row[0],
            "username": row[1]
        })
    conn.close()
    return reactions

def save_message_with_id(self, sender: str, recipient: str, message: str, timestamp: str, reply_to: int = None, file_url: str = None, file_type: str = None) -> int:
    """Save a message and return its ID."""
    conn = sqlite3.connect(self.db_path)
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO messages (sender, recipient, message, timestamp, reply_to, file_url, file_type) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (sender, recipient, message, timestamp, reply_to, file_url, file_type)
    )
    
    message_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return message_id

def get_group_messages_enhanced(self, limit: int = 100) -> List[Dict]:
    """Get group chat messages with enhanced fields."""
    conn = sqlite3.connect(self.db_path)
    cursor = conn.cursor()
    
    cursor.execute(
        """
        SELECT id, sender, message, timestamp, edited, deleted, reply_to, file_url, file_type
        FROM messages
        WHERE recipient = 'GROUP' AND deleted = 0
        ORDER BY timestamp DESC
        LIMIT ?
        """,
        (limit,)
    )
    
    messages = []
    for row in cursor.fetchall():
        msg = {
            "id": row[0],
            "sender": row[1],
            "message": row[2],
            "timestamp": row[3],
            "edited": bool(row[4]),
            "deleted": bool(row[5]),
            "reply_to": row[6],
            "file_url": row[7],
            "file_type": row[8],
            "reactions": self.get_message_reactions(row[0])
        }
        messages.append(msg)
    
    conn.close()
    return list(reversed(messages))

def get_private_messages_enhanced(self, user1: str, user2: str, limit: int = 100) -> List[Dict]:
    """Get private messages with enhanced fields."""
    conn = sqlite3.connect(self.db_path)
    cursor = conn.cursor()
    
    cursor.execute(
        """
        SELECT id, sender, message, timestamp, edited, deleted, reply_to, file_url, file_type
        FROM messages
        WHERE ((sender = ? AND recipient = ?) OR (sender = ? AND recipient = ?)) AND deleted = 0
        ORDER BY timestamp DESC
        LIMIT ?
        """,
        (user1, user2, user2, user1, limit)
    )
    
    messages = []
    for row in cursor.fetchall():
        msg = {
            "id": row[0],
            "sender": row[1],
            "message": row[2],
            "timestamp": row[3],
            "edited": bool(row[4]),
            "deleted": bool(row[5]),
            "reply_to": row[6],
            "file_url": row[7],
            "file_type": row[8],
            "reactions": self.get_message_reactions(row[0])
        }
        messages.append(msg)
    
    conn.close()
    return list(reversed(messages))

def search_messages(self, query: str, username: str = None) -> List[Dict]:
    """Search messages by content."""
    conn = sqlite3.connect(self.db_path)
    cursor = conn.cursor()
    
    if username:
        cursor.execute(
            """
            SELECT id, sender, recipient, message, timestamp
            FROM messages
            WHERE (sender = ? OR recipient = ?) AND message LIKE ? AND deleted = 0
            ORDER BY timestamp DESC
            LIMIT 50
            """,
            (username, username, f"%{query}%")
        )
    else:
        cursor.execute(
            """
            SELECT id, sender, recipient, message, timestamp
            FROM messages
            WHERE message LIKE ? AND deleted = 0
            ORDER BY timestamp DESC
            LIMIT 50
            """,
            (f"%{query}%",)
        )
    
    messages = []
    for row in cursor.fetchall():
        messages.append({
            "id": row[0],
            "sender": row[1],
            "recipient": row[2],
            "message": row[3],
            "timestamp": row[4]
        })
    
    conn.close()
    return messages

def mark_message_read(self, message_id: int, username: str):
    """Mark a message as read."""
    try:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        read_at = datetime.utcnow().isoformat()
        cursor.execute(
            "INSERT INTO read_receipts (message_id, username, read_at) VALUES (?, ?, ?)",
            (message_id, username, read_at)
        )
        conn.commit()
        conn.close()
    except sqlite3.IntegrityError:
        pass  # Already marked as read
