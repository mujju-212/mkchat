# ChatMK - Real-Time Chat Application Setup Guide

A modern, feature-rich real-time chat application with Discord/Slack-level features including typing indicators, reactions, file sharing, message editing, and more.

## 📋 Table of Contents
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Running the Server](#running-the-server)
- [Access Methods](#access-methods)
- [Network Sharing](#network-sharing)
- [Features](#features)
- [Documentation](#documentation)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Windows, macOS, or Linux

### Installation

1. **Clone or Download the Project**
   ```bash
   cd path/to/chatmk
   ```

2. **Create Virtual Environment (Recommended)**
   
   **Windows (PowerShell):**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
   
   **Windows (CMD):**
   ```cmd
   python -m venv venv
   venv\Scripts\activate.bat
   ```
   
   **macOS/Linux/Termux:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Running the Server

1. **Start the Application**
   ```bash
   python main.py
   ```

2. **Server Output**
   ```
   INFO:     Started server process
   INFO:     Uvicorn running on http://0.0.0.0:8000
   ```

3. **Open in Browser**
   - Local: `http://localhost:8000`
   - Network: `http://YOUR_LOCAL_IP:8000`

---

## 🌐 Access Methods

### 1. Local Access (Same Device)
Open your browser and go to:
```
http://localhost:8000
```

### 2. Local Network Access (Same WiFi)

**Find Your Local IP:**

**Windows (PowerShell):**
```powershell
ipconfig | Select-String "IPv4"
```

**macOS/Linux:**
```bash
ifconfig | grep "inet "
# or
ip addr show | grep "inet "
```

**Termux (Android):**
```bash
ifconfig wlan0 | grep "inet addr"
```

Then access from any device on the same network:
```
http://YOUR_LOCAL_IP:8000
```
Example: `http://192.168.1.100:8000`

---

## 🔗 Network Sharing Options

### Option A: Local Network Sharing (Within WiFi)

**Requirements:**
- All devices must be on the same WiFi network
- Server device firewall must allow incoming connections on port 8000

**Windows Firewall Rule (if needed):**
```powershell
New-NetFirewallRule -DisplayName "ChatMK Server" -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow
```

**Steps:**
1. Run the server: `python main.py`
2. Find your local IP (see above)
3. Share the URL: `http://YOUR_LOCAL_IP:8000`
4. Users on your WiFi can access directly from their mobile/desktop browsers

---

### Option B: Serveo Tunnel (Simple, No Installation)

**Free, no signup required. Perfect for quick sharing.**

1. **Start Your Server**
   ```bash
   python main.py
   ```

2. **Open New Terminal and Run Serveo**
   
   **Basic (Random subdomain):**
   ```bash
   ssh -R 80:localhost:8000 serveo.net
   ```
   
   **Custom subdomain:**
   ```bash
   ssh -R mychat:80:localhost:8000 serveo.net
   ```

3. **Share the URL**
   - Serveo will display: `https://random.serveo.net` or `https://mychat.serveo.net`
   - Share this URL with anyone, anywhere!

**Pros:**
- ✅ No installation required
- ✅ No account needed
- ✅ Works immediately
- ✅ HTTPS included

**Cons:**
- ⚠️ Random subdomain changes each time (unless you use custom)
- ⚠️ Connection may drop occasionally

---

### Option C: Cloudflare Tunnel (Recommended for Production)

**Free, stable, secure. Best for long-term use.**

1. **Install Cloudflare Tunnel**
   
   **Windows:**
   ```powershell
   # Download from: https://github.com/cloudflare/cloudflared/releases
   # Or use winget:
   winget install --id Cloudflare.cloudflared
   ```
   
   **macOS:**
   ```bash
   brew install cloudflared
   ```
   
   **Linux:**
   ```bash
   wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
   sudo dpkg -i cloudflared-linux-amd64.deb
   ```
   
   **Termux:**
   ```bash
   pkg install cloudflared
   ```

2. **Authenticate (One-time)**
   ```bash
   cloudflared tunnel login
   ```
   This opens a browser to log in with your Cloudflare account (free signup).

3. **Create a Tunnel**
   ```bash
   cloudflared tunnel create chatmk
   ```
   This creates a tunnel and generates credentials.

4. **Route Your Tunnel**
   ```bash
   cloudflared tunnel route dns chatmk chat.yourdomain.com
   ```
   Or use a free `.trycloudflare.com` subdomain:
   ```bash
   cloudflared tunnel --url http://localhost:8000
   ```

5. **Run the Tunnel**
   ```bash
   cloudflared tunnel run chatmk
   ```

6. **Quick Start (No Configuration)**
   ```bash
   cloudflared tunnel --url http://localhost:8000
   ```
   This gives you a temporary `https://xxx.trycloudflare.com` URL instantly!

**Pros:**
- ✅ Free forever
- ✅ Very stable connection
- ✅ Professional HTTPS
- ✅ Custom domain support
- ✅ DDoS protection
- ✅ Fast CDN

**Cons:**
- ⚠️ Requires Cloudflare account (free)
- ⚠️ Initial setup takes 2-3 minutes

---

### Option D: ngrok (Popular Alternative)

1. **Install ngrok**
   - Download from [ngrok.com](https://ngrok.com/download)
   - Or use package manager:
   ```bash
   # Windows (Chocolatey)
   choco install ngrok
   
   # macOS
   brew install ngrok
   
   # Linux (Snap)
   snap install ngrok
   ```

2. **Sign Up & Get Auth Token**
   - Create free account at [ngrok.com](https://ngrok.com)
   - Copy your authtoken from dashboard

3. **Add Auth Token**
   ```bash
   ngrok config add-authtoken YOUR_TOKEN_HERE
   ```

4. **Start Tunnel**
   ```bash
   ngrok http 8000
   ```

5. **Share the URL**
   - ngrok displays: `https://random-name.ngrok-free.app`
   - Share this URL with anyone!

**Pros:**
- ✅ Very popular and reliable
- ✅ Great web interface
- ✅ Request inspection tools

**Cons:**
- ⚠️ Free tier shows "Visit Site" button to visitors
- ⚠️ URL changes on each restart (paid plans get static URLs)

---

## 📱 Mobile Access

All sharing methods work perfectly on mobile devices:

1. **Local Network:** Just open the shared URL in mobile browser
2. **Serveo/Cloudflare/ngrok:** Works on any mobile device with internet
3. **Progressive Web App:** Add to home screen for app-like experience

**Add to Home Screen:**
- **iOS Safari:** Tap share → "Add to Home Screen"
- **Android Chrome:** Tap menu → "Add to Home Screen"

---

## ✨ Features

- 💬 Real-time messaging (WebSocket)
- 👥 Group chat and private DMs
- ⌨️ Typing indicators
- 😊 Message reactions
- ✏️ Edit and delete messages
- 💾 Reply to messages
- 📎 File upload (images, PDFs, documents)
- 🔍 Message search
- ✓✓ Delivery indicators
- 🟢 Online/offline status
- 🎨 Beautiful purple gradient theme
- 📱 Fully responsive mobile design
- 🔒 Session persistence
- 🌙 Glass morphism UI

---

## 📚 Documentation

Additional documentation is available in the `docs/` folder:

- **[FEATURES_SUMMARY.md](docs/FEATURES_SUMMARY.md)** - Complete feature list
- **[ENHANCED_FEATURES.md](docs/ENHANCED_FEATURES.md)** - Detailed feature guide
- **[QUICK_REFERENCE.md](docs/QUICK_REFERENCE.md)** - API and shortcuts
- **[WHATS_NEW.md](docs/WHATS_NEW.md)** - Changelog and updates
- **[IMPLEMENTATION_PLAN.md](docs/IMPLEMENTATION_PLAN.md)** - Technical details

---

## 🛠️ Troubleshooting

### Server won't start
- Check if port 8000 is already in use
- Verify Python version: `python --version` (need 3.8+)
- Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`

### Can't connect from other devices
- Verify firewall allows port 8000
- Check if devices are on same WiFi network
- Try using tunnel service (Serveo/Cloudflare/ngrok)

### Files won't upload
- Check `uploads/` folder exists and is writable
- Verify `python-multipart` is installed: `pip install python-multipart`

---

## 🔒 Security Notes

- Default setup is for local/development use
- For production deployment:
  - Enable HTTPS
  - Add authentication middleware
  - Configure CORS properly
  - Use environment variables for sensitive data
  - Set up proper database backups
  - Use a production WSGI server (gunicorn, etc.)

---

## 📄 License

This project is open source and available for personal and educational use.

---

## 💡 Tips

1. **Keep server running:** Use `screen` or `tmux` on Linux/Termux
   ```bash
   screen -S chatmk
   python main.py
   # Press Ctrl+A, then D to detach
   # screen -r chatmk to reattach
   ```

2. **Auto-restart on crash:** Use `systemd` service (Linux) or Task Scheduler (Windows)

3. **Custom domain:** Use Cloudflare tunnel with your own domain

4. **Performance:** For 100+ users, consider using Redis for session management

---

**🎉 Happy Chatting! Enjoy your Discord-level chat application!**
