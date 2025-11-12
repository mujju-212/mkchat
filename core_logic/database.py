import sqlite3
import hashlib
from typing import List, Dict
from datetime import datetime


class Database:
    """Database handler for chat application using SQLite."""
    
    def __init__(self, db_path: str = "chat_history.db"):
        self.db_path = db_path
        self._init_database()

    def _get_connection(self):
        """Get database connection with timeout and optimized settings."""
        conn = sqlite3.connect(self.db_path, timeout=30.0, check_same_thread=False)
        conn.execute("PRAGMA journal_mode=WAL")  # Write-Ahead Logging for better concurrency
        conn.execute("PRAGMA busy_timeout=30000")  # 30 second timeout
        return conn

    def _init_database(self):
        """Initialize database tables."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL,
                avatar_color TEXT DEFAULT '#6366f1',
                status TEXT DEFAULT 'online',
                status_message TEXT DEFAULT ''
            )
        """)
        
        # Messages table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender TEXT NOT NULL,
                recipient TEXT NOT NULL,
                message TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                edited INTEGER DEFAULT 0,
                deleted INTEGER DEFAULT 0,
                reply_to INTEGER DEFAULT NULL,
                file_url TEXT DEFAULT NULL,
                file_type TEXT DEFAULT NULL,
                FOREIGN KEY (sender) REFERENCES users(username),
                FOREIGN KEY (reply_to) REFERENCES messages(id)
            )
        """)
        
        # Reactions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message_id INTEGER NOT NULL,
                username TEXT NOT NULL,
                emoji TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (message_id) REFERENCES messages(id),
                FOREIGN KEY (username) REFERENCES users(username),
                UNIQUE(message_id, username, emoji)
            )
        """)
        
        # Read receipts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS read_receipts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message_id INTEGER NOT NULL,
                username TEXT NOT NULL,
                read_at TEXT NOT NULL,
                FOREIGN KEY (message_id) REFERENCES messages(id),
                FOREIGN KEY (username) REFERENCES users(username),
                UNIQUE(message_id, username)
            )
        """)
        
        conn.commit()
        conn.close()

    def _hash_password(self, password: str) -> str:
        """Hash password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()

    def create_user(self, username: str, password: str) -> bool:
        """Create a new user."""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            password_hash = self._hash_password(password)
            created_at = datetime.now().isoformat()
            
            cursor.execute(
                "INSERT INTO users (username, password_hash, created_at) VALUES (?, ?, ?)",
                (username, password_hash, created_at)
            )
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False

    def verify_user(self, username: str, password: str) -> bool:
        """Verify user credentials."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        password_hash = self._hash_password(password)
        
        cursor.execute(
            "SELECT password_hash FROM users WHERE username = ?",
            (username,)
        )
        
        result = cursor.fetchone()
        conn.close()
        
        if result and result[0] == password_hash:
            return True
        return False

    def user_exists(self, username: str) -> bool:
        """Check if user exists."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        
        conn.close()
        return result is not None

    def get_all_users(self) -> List[str]:
        """Get all registered usernames."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT username FROM users ORDER BY username")
        users = [row[0] for row in cursor.fetchall()]
        
        conn.close()
        return users

    def save_message(self, sender: str, recipient: str, message: str, timestamp: str):
        """Save a message to database."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO messages (sender, recipient, message, timestamp) VALUES (?, ?, ?, ?)",
            (sender, recipient, message, timestamp)
        )
        
        conn.commit()
        conn.close()

    def get_group_messages(self, limit: int = 100) -> List[Dict]:
        """Get group chat messages."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            SELECT sender, message, timestamp
            FROM messages
            WHERE recipient = 'GROUP'
            ORDER BY timestamp DESC
            LIMIT ?
            """,
            (limit,)
        )
        
        messages = []
        for row in cursor.fetchall():
            messages.append({
                "sender": row[0],
                "message": row[1],
                "timestamp": row[2]
            })
        
        conn.close()
        return list(reversed(messages))

    def get_private_messages(self, user1: str, user2: str, limit: int = 100) -> List[Dict]:
        """Get private messages between two users."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            SELECT sender, message, timestamp
            FROM messages
            WHERE (sender = ? AND recipient = ?) OR (sender = ? AND recipient = ?)
            ORDER BY timestamp DESC
            LIMIT ?
            """,
            (user1, user2, user2, user1, limit)
        )
        
        messages = []
        for row in cursor.fetchall():
            messages.append({
                "sender": row[0],
                "message": row[1],
                "timestamp": row[2]
            })
        
        conn.close()
        return list(reversed(messages))

    def get_total_users(self) -> int:
        """Get total number of registered users."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def get_total_messages(self) -> int:
        """Get total number of messages."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM messages")
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def get_messages_today(self) -> int:
        """Get number of messages sent today."""
        conn = self._get_connection()
        cursor = conn.cursor()
        today = datetime.now().date().isoformat()
        cursor.execute(
            "SELECT COUNT(*) FROM messages WHERE DATE(timestamp) = ?",
            (today,)
        )
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def get_group_message_count(self) -> int:
        """Get total number of group messages."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM messages WHERE recipient = 'GROUP'")
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def get_all_users_with_stats(self) -> List[Dict]:
        """Get all users with their message counts."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                u.username,
                u.created_at,
                COUNT(m.id) as message_count
            FROM users u
            LEFT JOIN messages m ON u.username = m.sender
            GROUP BY u.username, u.created_at
            ORDER BY message_count DESC
        """)
        
        users = []
        for row in cursor.fetchall():
            users.append({
                "username": row[0],
                "created_at": row[1],
                "message_count": row[2]
            })
        
        conn.close()
        return users

    def get_all_messages(self, limit: int = 500) -> List[Dict]:
        """Get all messages from the system."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT sender, recipient, message, timestamp
            FROM messages
            ORDER BY timestamp DESC
            LIMIT ?
        """, (limit,))
        
        messages = []
        for row in cursor.fetchall():
            messages.append({
                "sender": row[0],
                "recipient": row[1],
                "message": row[2],
                "timestamp": row[3]
            })
        
        conn.close()
        return list(reversed(messages))
    # Enhanced Features Methods
    
    def update_user_status(self, username: str, status: str, status_message: str = ''):
        '''Update user status.'''
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE users SET status = ?, status_message = ? WHERE username = ?',
            (status, status_message, username)
        )
        conn.commit()
        conn.close()

    def get_user_info(self, username: str) -> Dict:
        '''Get user information.'''
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT username, avatar_color, status, status_message FROM users WHERE username = ?',
            (username,)
        )
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'username': result[0],
                'avatar_color': result[1],
                'status': result[2],
                'status_message': result[3]
            }
        return None

    def update_message(self, message_id: int, new_text: str):
        '''Edit a message.'''
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE messages SET message = ?, edited = 1 WHERE id = ?',
            (new_text, message_id)
        )
        conn.commit()
        conn.close()

    def delete_message(self, message_id: int):
        '''Delete a message (soft delete).'''
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE messages SET deleted = 1 WHERE id = ?',
            (message_id,)
        )
        conn.commit()
        conn.close()

    def add_reaction(self, message_id: int, username: str, emoji: str):
        '''Add a reaction to a message.'''
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            timestamp = datetime.now().isoformat()
            cursor.execute(
                'INSERT INTO reactions (message_id, username, emoji, timestamp) VALUES (?, ?, ?, ?)',
                (message_id, username, emoji, timestamp)
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            # Reaction already exists, remove it
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(
                'DELETE FROM reactions WHERE message_id = ? AND username = ? AND emoji = ?',
                (message_id, username, emoji)
            )
            conn.commit()
            conn.close()
            return False

    def get_message_reactions(self, message_id: int) -> List[Dict]:
        '''Get reactions for a message.'''
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT emoji, username FROM reactions WHERE message_id = ?',
            (message_id,)
        )
        reactions = []
        for row in cursor.fetchall():
            reactions.append({
                'emoji': row[0],
                'username': row[1]
            })
        conn.close()
        return reactions

    def save_message_with_id(self, sender: str, recipient: str, message: str, timestamp: str, reply_to: int = None, file_url: str = None, file_type: str = None) -> int:
        '''Save a message and return its ID.'''
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            'INSERT INTO messages (sender, recipient, message, timestamp, reply_to, file_url, file_type) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (sender, recipient, message, timestamp, reply_to, file_url, file_type)
        )
        
        message_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return message_id

    def get_group_messages_enhanced(self, limit: int = 100) -> List[Dict]:
        '''Get group chat messages with enhanced fields.'''
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            '''
            SELECT id, sender, message, timestamp, edited, deleted, reply_to, file_url, file_type
            FROM messages
            WHERE recipient = 'GROUP' AND deleted = 0
            ORDER BY timestamp DESC
            LIMIT ?
            ''',
            (limit,)
        )
        
        messages = []
        for row in cursor.fetchall():
            msg = {
                'id': row[0],
                'sender': row[1],
                'message': row[2],
                'timestamp': row[3],
                'edited': bool(row[4]),
                'deleted': bool(row[5]),
                'reply_to': row[6],
                'file_url': row[7],
                'file_type': row[8],
                'reactions': self.get_message_reactions(row[0])
            }
            messages.append(msg)
        
        conn.close()
        return list(reversed(messages))

    def get_private_messages_enhanced(self, user1: str, user2: str, limit: int = 100) -> List[Dict]:
        '''Get private messages with enhanced fields.'''
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            '''
            SELECT id, sender, message, timestamp, edited, deleted, reply_to, file_url, file_type
            FROM messages
            WHERE ((sender = ? AND recipient = ?) OR (sender = ? AND recipient = ?)) AND deleted = 0
            ORDER BY timestamp DESC
            LIMIT ?
            ''',
            (user1, user2, user2, user1, limit)
        )
        
        messages = []
        for row in cursor.fetchall():
            msg = {
                'id': row[0],
                'sender': row[1],
                'message': row[2],
                'timestamp': row[3],
                'edited': bool(row[4]),
                'deleted': bool(row[5]),
                'reply_to': row[6],
                'file_url': row[7],
                'file_type': row[8],
                'reactions': self.get_message_reactions(row[0])
            }
            messages.append(msg)
        
        conn.close()
        return list(reversed(messages))

    def search_messages(self, query: str, username: str = None) -> List[Dict]:
        '''Search messages by content.'''
        conn = self._get_connection()
        cursor = conn.cursor()
        
        if username:
            cursor.execute(
                '''
                SELECT id, sender, recipient, message, timestamp
                FROM messages
                WHERE (sender = ? OR recipient = ?) AND message LIKE ? AND deleted = 0
                ORDER BY timestamp DESC
                LIMIT 50
                ''',
                (username, username, f'%{query}%')
            )
        else:
            cursor.execute(
                '''
                SELECT id, sender, recipient, message, timestamp
                FROM messages
                WHERE message LIKE ? AND deleted = 0
                ORDER BY timestamp DESC
                LIMIT 50
                ''',
                (f'%{query}%',)
            )
        
        messages = []
        for row in cursor.fetchall():
            messages.append({
                'id': row[0],
                'sender': row[1],
                'recipient': row[2],
                'message': row[3],
                'timestamp': row[4]
            })
        
        conn.close()
        return messages

    def mark_message_read(self, message_id: int, username: str):
        '''Mark a message as read.'''
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            read_at = datetime.now().isoformat()
            cursor.execute(
                'INSERT INTO read_receipts (message_id, username, read_at) VALUES (?, ?, ?)',
                (message_id, username, read_at)
            )
            conn.commit()
            conn.close()
        except sqlite3.IntegrityError:
            pass  # Already marked as read

