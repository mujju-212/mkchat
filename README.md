# 💬 ChatMK - Real-Time Chat Application

A modern, feature-rich real-time chat application with Discord/Slack-level features built with FastAPI and WebSockets.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

---

## ✨ Features

- 💬 **Real-time messaging** with WebSocket technology
- 👥 **Group chat** and **private direct messages**
- ⌨️ **Typing indicators** - See when others are typing
- 😊 **Message reactions** - React with emojis
- ✏️ **Edit messages** - Fix typos anytime
- 🗑️ **Delete messages** - Remove unwanted messages
- 💬 **Reply to messages** - Thread conversations
- 📎 **File upload** - Share images, PDFs, documents (all file types)
- 🔍 **Search messages** - Find old conversations
- ✓✓ **Delivery indicators** - Know when messages are sent
- 🟢 **Online/offline status** - See who's available
- 🎨 **Beautiful UI** - Purple gradient theme with glass morphism
- 📱 **Mobile responsive** - Works perfectly on phones and tablets
- 🔒 **Session persistence** - Stay logged in across refreshes
- 🚀 **Fast and lightweight** - Built for performance

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package installer

### Installation

1. **Clone the repository**
   ```bash
   cd chatmk
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   .\venv\Scripts\Activate.ps1
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the server**
   ```bash
   python main.py
   ```

5. **Open in browser**
   ```
   http://localhost:8000
   ```

That's it! 🎉

---

## 📖 Documentation

Comprehensive documentation is available:

### 📘 Getting Started
- **[docs/QUICK_START.md](docs/QUICK_START.md)** - ⚡ Quick reference card with all commands
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - 📝 Complete setup instructions
- **[docs/SHARING_GUIDE.md](docs/SHARING_GUIDE.md)** - 🌐 Detailed guide for sharing (local/internet)

### 📚 Features & Usage
- **[docs/FEATURES_SUMMARY.md](docs/FEATURES_SUMMARY.md)** - Feature overview
- **[docs/ENHANCED_FEATURES.md](docs/ENHANCED_FEATURES.md)** - Detailed feature guide
- **[docs/QUICK_REFERENCE.md](docs/QUICK_REFERENCE.md)** - API and shortcuts
- **[docs/WHATS_NEW.md](docs/WHATS_NEW.md)** - Changelog

### 🏗️ Technical
- **[docs/IMPLEMENTATION_PLAN.md](docs/IMPLEMENTATION_PLAN.md)** - Architecture details
- **[docs/README.md](docs/README.md)** - Documentation index

---

## 🌐 Sharing Your Chat

### Local Network (Same WiFi)
Share with friends on the same WiFi:
```
http://YOUR_LOCAL_IP:8000
```

### Internet Sharing Options

#### 1. Serveo (Easiest - No Installation)
```bash
ssh -R 80:localhost:8000 serveo.net
```

#### 2. Cloudflare Tunnel (Recommended)
```bash
cloudflared tunnel --url http://localhost:8000
```

#### 3. ngrok
```bash
ngrok http 8000
```

**See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed instructions on all sharing methods.**

---

## 📱 Mobile Access

Works perfectly on mobile devices:
1. Access via local network or internet tunnel
2. Add to home screen for app-like experience
3. Fully responsive design optimized for mobile

---

## 🛠️ Tech Stack

- **Backend:** FastAPI (Python)
- **Real-time:** WebSockets
- **Database:** SQLite
- **Frontend:** Vanilla JavaScript, HTML5, Tailwind CSS
- **File Upload:** python-multipart
- **Server:** Uvicorn (ASGI)

---

## 📂 Project Structure

```
chatmk/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── SETUP_GUIDE.md         # Setup instructions
├── README.md              # This file
│
├── core_logic/            # Backend logic
│   ├── __init__.py
│   ├── database.py        # SQLite database handler
│   ├── leaky_bucket.py    # Rate limiting
│   └── managers.py        # Connection manager
│
├── templates/             # HTML templates
│   ├── chat.html          # Main chat interface
│   └── admin.html         # Admin dashboard
│
├── uploads/               # Uploaded files storage
│
└── docs/                  # Documentation
    ├── README.md
    ├── FEATURES_SUMMARY.md
    ├── ENHANCED_FEATURES.md
    ├── QUICK_REFERENCE.md
    ├── WHATS_NEW.md
    └── IMPLEMENTATION_PLAN.md
```

---

## 🎨 Screenshots

### Welcome Screen
<div align="center">
  <img src="docs/images/Screenshot 2025-11-10 005156.png" alt="MK Chat Welcome Screen" width="300"/>
  <p><i>Clean, modern welcome screen with feature highlights</i></p>
</div>

**Features shown:**
- 💬 Real-time messaging
- 💾 Persistent chat history
- 🛡️ Spam protection
- 👥 Group & private chats

---

### Chat Interface
<div align="center">
  <img src="docs/images/Screenshot 2025-11-10 005215.png" alt="MK Chat Interface" width="300"/>
  <p><i>Beautiful purple gradient theme with message history</i></p>
</div>

**Features visible:**
- 📎 File upload support (PDF shown)
- ✓✓ Delivery indicators
- ⏰ Relative timestamps ("40m ago", "27m ago")
- 🟢 Online/offline status
- 🔍 Search functionality
- 💬 Clean message bubbles

---

### Sidebar & Navigation
<div align="center">
  <img src="docs/images/Screenshot 2025-11-10 005234.png" alt="MK Chat Sidebar" width="300"/>
  <p><i>Organized sidebar with user management</i></p>
</div>

**Features shown:**
- 👤 Current user display with online indicator
- 💬 Group Chat access
- 👥 Online Users list with status
- 🎨 Avatar with initial letters
- 🚪 Logout button

---

### File Sharing & Messages
<div align="center">
  <img src="docs/images/Screenshot 2025-11-10 005243.png" alt="File Sharing Feature" width="300"/>
  <p><i>Seamless file sharing with type-specific icons</i></p>
</div>

**Features demonstrated:**
- 📎 File upload with paperclip icon
- 📕 PDF file preview cards
- 💬 Mixed text and file messages
- ⏰ Smart timestamps
- ✓✓ Read receipts
- 👤 Sender identification

---

## 📱 Mobile Responsive
- Fully responsive design
- Touch-optimized controls
- Same features as desktop

---

## ⚙️ Configuration

The application uses sensible defaults and requires no configuration for basic use.

**Default Settings:**
- Port: 8000
- Database: `chat_history.db` (SQLite)
- Upload folder: `uploads/`
- Max connections: Unlimited (rate-limited)

---

## 🔒 Security Notes

**Current setup is designed for:**
- Local development
- Private networks
- Trusted users

**For production deployment, consider:**
- Adding user authentication
- Enabling HTTPS
- Configuring CORS
- Setting file upload limits
- Using a production database (PostgreSQL)
- Implementing proper session management
- Adding rate limiting per user

---

## 🐛 Troubleshooting

### Server won't start
```bash
# Check if port 8000 is in use
# Windows
netstat -ano | findstr :8000

# macOS/Linux
lsof -i :8000

# Kill process and restart
```

### Can't connect from other devices
1. Check firewall settings
2. Verify devices are on same network
3. Try using a tunnel service (Serveo/Cloudflare)

### Files won't upload
```bash
# Reinstall python-multipart
pip install python-multipart --force-reinstall
```

---

## 📝 License

This project is open source and available for personal and educational use.

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

---

## 💡 Tips

1. **Use screen/tmux for persistent sessions**
   ```bash
   screen -S chatmk
   python main.py
   # Ctrl+A, D to detach
   ```

2. **Monitor logs in real-time**
   ```bash
   python main.py 2>&1 | tee chat.log
   ```

3. **Custom domain with Cloudflare**
   - Free HTTPS
   - Professional look
   - CDN benefits

---

## 📞 Support

- Check [SETUP_GUIDE.md](SETUP_GUIDE.md) for setup help
- Review [docs/](docs/) for feature documentation
- Ensure you're using the latest version

---

## 🎉 Acknowledgments

Built with modern web technologies for real-time communication.

---

**Made with ❤️ for seamless real-time chatting**

---

## 🔗 Quick Links

- [Setup Guide](SETUP_GUIDE.md)
- [Documentation](docs/README.md)
- [Requirements](requirements.txt)

---

**Current Version:** 2.0  
**Last Updated:** November 10, 2025