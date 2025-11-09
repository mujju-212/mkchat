# MK Chat - Real-Time Messaging Platform

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![WebSocket](https://img.shields.io/badge/WebSocket-Real--time-orange.svg)](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A modern, feature-rich real-time chat application with Discord/Slack-level features built with FastAPI and WebSockets. Perfect for teams, communities, or personal use.

## 🌟 Highlights

- **Real-time Communication** - Instant messaging with WebSocket technology
- **Discord-Level Features** - Typing indicators, reactions, file sharing, message editing
- **Beautiful UI** - Purple gradient theme with glass morphism effects
- **Mobile First** - Fully responsive design optimized for all devices
- **Easy Deployment** - Share locally or over the internet with Serveo/Cloudflare/ngrok
- **No Database Setup** - Uses SQLite, works out of the box

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/chatmk.git
cd chatmk

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\Activate.ps1  # Windows

# Install dependencies
pip install -r requirements.txt

# Run the server
python main.py
```

Open http://localhost:8000 in your browser and start chatting!

## ✨ Key Features

### 💬 Messaging
- Real-time bidirectional communication
- Group chat and private direct messages
- Message search and history
- Reply to messages (threading)
- Edit and delete messages
- Delivery indicators (✓✓)

### 🎨 User Experience
- Typing indicators
- Message reactions with emojis
- Online/offline status
- Relative timestamps ("5m ago", "Yesterday")
- Glass morphism UI design
- Smooth animations and transitions

### 📎 File Sharing
- Upload any file type
- Type-specific icons (PDF, Word, Excel, etc.)
- Image preview
- Download capability
- File size display

### 🔒 Security & Performance
- Rate limiting (Leaky Bucket algorithm)
- Session persistence
- Spam protection
- Efficient SQLite database
- WebSocket connection management

## 🌐 Deployment Options

### Local Network (Same WiFi)
```bash
# Access from any device on your network
http://YOUR_LOCAL_IP:8000
```

### Internet Sharing

**Serveo (Easiest - No Installation)**
```bash
ssh -R 80:localhost:8000 serveo.net
```

**Cloudflare Tunnel (Recommended)**
```bash
cloudflared tunnel --url http://localhost:8000
```

**ngrok**
```bash
ngrok http 8000
```

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed instructions.

## 📱 Mobile Support

- Fully responsive design
- Touch-optimized controls
- Add to home screen for app-like experience
- Works on iOS, Android, and all modern browsers

## 🛠️ Tech Stack

- **Backend:** FastAPI (Python)
- **Real-time:** WebSockets
- **Database:** SQLite
- **Frontend:** Vanilla JavaScript, HTML5, Tailwind CSS
- **File Upload:** python-multipart
- **Server:** Uvicorn (ASGI)

## 📚 Documentation

- [Setup Guide](SETUP_GUIDE.md) - Installation and configuration
- [Sharing Guide](docs/SHARING_GUIDE.md) - How to share your chat
- [Quick Start](docs/QUICK_START.md) - Quick reference card
- [Features](docs/FEATURES_SUMMARY.md) - Complete feature list
- [API Reference](docs/QUICK_REFERENCE.md) - Developer documentation

## 🎨 Screenshots

See the main [README.md](README.md) for detailed screenshots of:
- Welcome screen
- Chat interface
- Sidebar navigation
- File sharing

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

Built with modern web technologies for seamless real-time communication.

## 📞 Support

For issues or questions:
1. Check the [SETUP_GUIDE.md](SETUP_GUIDE.md)
2. Review [docs/](docs/) folder
3. Open an issue on GitHub

---

**⭐ If you find this project useful, please consider giving it a star!**

Made with ❤️ for the community
