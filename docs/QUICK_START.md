# 🚀 ChatMK - Quick Start Card

```
╔═══════════════════════════════════════════════════════════════════╗
║                    ChatMK Chat Application                        ║
║              Real-Time Messaging for Everyone                     ║
╚═══════════════════════════════════════════════════════════════════╝
```

## 📦 Installation (One Time)

```bash
# 1. Navigate to project folder
cd path/to/chatmk

# 2. Create virtual environment
python -m venv venv

# 3. Activate it
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Windows CMD:
venv\Scripts\activate.bat
# Mac/Linux/Termux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt
```

---

## ▶️ Start Server

```bash
python main.py
```

**You'll see:**
```
======================================================================
🚀 ChatMK - Real-Time Chat Application
======================================================================

📍 ACCESS YOUR CHAT:
----------------------------------------------------------------------
   🏠 Local (this device):     http://localhost:8000
   📱 Network (same WiFi):     http://192.168.1.XX:8000

🌐 SHARE OVER THE INTERNET:
   Option 1: Serveo        → ssh -R 80:localhost:8000 serveo.net
   Option 2: Cloudflare    → cloudflared tunnel --url http://localhost:8000
   Option 3: ngrok         → ngrok http 8000
======================================================================
```

---

## 🌐 Sharing Cheat Sheet

### Same WiFi (Local Network)
```
Share: http://YOUR_IP:8000
Example: http://192.168.1.74:8000
```

### Over Internet

**Serveo (Easiest):**
```bash
ssh -R 80:localhost:8000 serveo.net
```
→ Share the `https://xxxxx.serveo.net` URL

**Cloudflare (Best):**
```bash
cloudflared tunnel --url http://localhost:8000
```
→ Share the `https://xxx.trycloudflare.com` URL

**ngrok:**
```bash
ngrok http 8000
```
→ Share the `https://xxx.ngrok-free.app` URL

---

## 📁 Project Structure

```
chatmk/
├── 📄 README.md              # Project overview
├── 📄 SETUP_GUIDE.md         # Detailed setup instructions
├── 📄 SHARING_GUIDE.md       # Complete sharing reference
├── 📄 requirements.txt       # Python dependencies
├── 🐍 main.py                # Application entry point
│
├── 📂 docs/                  # Documentation
│   ├── FEATURES_SUMMARY.md
│   ├── ENHANCED_FEATURES.md
│   ├── QUICK_REFERENCE.md
│   ├── WHATS_NEW.md
│   └── IMPLEMENTATION_PLAN.md
│
├── 📂 core_logic/            # Backend code
├── 📂 templates/             # HTML files
└── 📂 uploads/               # Uploaded files
```

---

## ⚡ Common Commands

```bash
# Start server
python main.py

# Check if running
# Windows:
netstat -ano | findstr :8000
# Mac/Linux:
lsof -i :8000

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Update packages
pip install --upgrade fastapi uvicorn
```

---

## 🎯 Features at a Glance

✅ Real-time messaging (WebSocket)
✅ Group chat & private DMs
✅ Typing indicators
✅ Message reactions (😊)
✅ Edit & delete messages
✅ Reply to messages
✅ File uploads (all types)
✅ Search messages
✅ Online/offline status
✅ Beautiful mobile UI
✅ Session persistence

---

## 🆘 Quick Fixes

**Server won't start:**
```bash
# Kill existing process
# Windows:
taskkill /F /IM python.exe
# Mac/Linux:
pkill python
```

**Port already in use:**
```python
# Edit main.py, change port from 8000 to 8001
uvicorn.run(app, host="0.0.0.0", port=8001)
```

**Can't connect from phone:**
```bash
# Check firewall (Windows)
New-NetFirewallRule -DisplayName "ChatMK" -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow
```

---

## 📚 Documentation Links

| Document | Purpose |
|----------|---------|
| **README.md** | Project overview & quick start |
| **SETUP_GUIDE.md** | Complete installation guide |
| **SHARING_GUIDE.md** | Detailed sharing methods |
| **docs/FEATURES_SUMMARY.md** | All features explained |
| **docs/ENHANCED_FEATURES.md** | Feature usage guide |

---

## 🎨 Access Points

```
┌─────────────────────────────────────────────────┐
│  Access Method     │  URL Format                │
├────────────────────┼────────────────────────────┤
│  Local Device      │  http://localhost:8000     │
│  Same WiFi         │  http://192.168.x.x:8000   │
│  Serveo Tunnel     │  https://xxx.serveo.net    │
│  Cloudflare Tunnel │  https://xxx.trycloudflare │
│  ngrok Tunnel      │  https://xxx.ngrok-free    │
└─────────────────────────────────────────────────┘
```

---

## 🔐 Default Setup

```
Port:           8000
Database:       chat_history.db (SQLite)
Upload folder:  uploads/
Admin page:     http://localhost:8000/admin
Max file size:  Unlimited (configure as needed)
```

---

## 💡 Pro Tips

1. **Keep terminal open** while server is running
2. **Bookmark admin page** for monitoring: `/admin`
3. **Use Cloudflare** for stable long-term sharing
4. **Use Serveo** for quick demos
5. **Add to home screen** on mobile for app-like feel

---

## 🚦 Status Check

```bash
# Server running? Look for:
INFO:     Uvicorn running on http://0.0.0.0:8000

# Connections active? Look for:
INFO:     connection open

# Ready to share when you see the banner!
```

---

## 📱 Mobile Setup

1. Open URL in mobile browser
2. Tap menu (⋮ or share button)
3. Select "Add to Home Screen"
4. Enjoy app-like experience!

---

```
╔═══════════════════════════════════════════════════════════════════╗
║  🎉 You're all set! Happy chatting!                              ║
║                                                                   ║
║  Need help? Check SETUP_GUIDE.md or docs/README.md              ║
╚═══════════════════════════════════════════════════════════════════╝
```

**Version:** 2.0  
**Updated:** November 10, 2025