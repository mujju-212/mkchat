# 🌐 ChatMK Sharing Guide

Quick reference for sharing your chat application with others.

---

## 🏠 Local Access (Same Device)

Access from the device running the server:

```
http://localhost:8000
http://127.0.0.1:8000
```

---

## 📱 Network Access (Same WiFi)

### Find Your Local IP

**Windows (PowerShell):**
```powershell
ipconfig | Select-String "IPv4"
```

**macOS/Linux:**
```bash
ifconfig | grep "inet "
```

**Termux (Android):**
```bash
ifconfig wlan0 | grep "inet addr"
```

### Share the URL
Once you find your IP (e.g., 192.168.1.74), share:
```
http://YOUR_IP:8000
```

**Example:** `http://192.168.1.74:8000`

**Requirements:**
- Both devices must be on the same WiFi network
- Firewall must allow port 8000

---

## 🌍 Internet Sharing (Access from Anywhere)

### Option 1: Serveo ⭐ (Recommended for Quick Sharing)

**Advantages:**
- ✅ No installation required
- ✅ No signup needed
- ✅ Instant HTTPS
- ✅ Works immediately

**Steps:**
1. Keep your ChatMK server running
2. Open a **NEW** terminal/command prompt
3. Run one of these commands:

**Random subdomain:**
```bash
ssh -R 80:localhost:8000 serveo.net
```

**Custom subdomain:**
```bash
ssh -R mychat:80:localhost:8000 serveo.net
```

4. Serveo will display a URL like: `https://serveo.net` or `https://mychat.serveo.net`
5. Share that URL with anyone!

**Notes:**
- URL changes each time (unless using custom subdomain)
- May disconnect occasionally
- Free forever

---

### Option 2: Cloudflare Tunnel (Best for Stability)

**Advantages:**
- ✅ Very stable
- ✅ Professional HTTPS
- ✅ Custom domain support
- ✅ CDN benefits
- ✅ DDoS protection

**Installation:**

**Windows:**
```powershell
winget install --id Cloudflare.cloudflared
```
Or download from: https://github.com/cloudflare/cloudflared/releases

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

**Quick Start (No Configuration):**
1. Keep your ChatMK server running
2. Open a **NEW** terminal
3. Run:
```bash
cloudflared tunnel --url http://localhost:8000
```
4. Share the `https://xxx.trycloudflare.com` URL it displays!

**With Account (Permanent URLs):**
1. Sign up at https://dash.cloudflare.com/
2. Authenticate:
```bash
cloudflared tunnel login
```
3. Create tunnel:
```bash
cloudflared tunnel create chatmk
```
4. Run tunnel:
```bash
cloudflared tunnel run chatmk
```

---

### Option 3: ngrok (Popular Alternative)

**Advantages:**
- ✅ Very popular
- ✅ Great web interface
- ✅ Request inspection
- ✅ Replay functionality

**Installation:**

Download from: https://ngrok.com/download

Or use package managers:
```bash
# Windows (Chocolatey)
choco install ngrok

# macOS
brew install ngrok

# Linux (Snap)
snap install ngrok
```

**Setup:**
1. Sign up at https://ngrok.com/signup
2. Get your authtoken from https://dashboard.ngrok.com/get-started/your-authtoken
3. Add auth token:
```bash
ngrok config add-authtoken YOUR_TOKEN_HERE
```

**Usage:**
1. Keep your ChatMK server running
2. Open a **NEW** terminal
3. Run:
```bash
ngrok http 8000
```
4. Share the `https://xxx.ngrok-free.app` URL!

**Notes:**
- Free tier shows "Visit Site" button to visitors
- URL changes on each restart (paid plans get static URLs)
- Has web interface at http://localhost:4040

---

## 📱 Mobile Access Tips

### Add to Home Screen
Make ChatMK feel like a native app:

**iOS (Safari):**
1. Open the chat URL
2. Tap the Share button
3. Tap "Add to Home Screen"

**Android (Chrome):**
1. Open the chat URL
2. Tap the menu (⋮)
3. Tap "Add to Home Screen"

### Mobile Browser Tips
- Works in any mobile browser (Chrome, Safari, Firefox, etc.)
- All features work on mobile
- Responsive design optimized for phones
- Touch gestures supported

---

## 🔥 Quick Comparison

| Method | Setup Time | Stability | Custom Domain | Free | Best For |
|--------|-----------|-----------|---------------|------|----------|
| **Local Network** | 0 min | ⭐⭐⭐⭐⭐ | ❌ | ✅ | Same WiFi users |
| **Serveo** | 0 min | ⭐⭐⭐ | Limited | ✅ | Quick sharing |
| **Cloudflare** | 2-3 min | ⭐⭐⭐⭐⭐ | ✅ | ✅ | Production use |
| **ngrok** | 2 min | ⭐⭐⭐⭐ | 💰 Paid | ✅ Free tier | Development |

---

## 🛡️ Security Tips

### For Local Network Sharing
- Ensure you trust all users on your WiFi
- Use strong passwords for user accounts
- Monitor active connections

### For Internet Sharing
- Change default admin credentials
- Monitor who you share links with
- Consider setting up user authentication
- For sensitive use, enable HTTPS only
- Keep your server updated

### Production Deployment
If deploying for real-world use:
- Use environment variables for secrets
- Set up proper database backups
- Configure rate limiting per user
- Enable CORS properly
- Use a production WSGI server
- Consider adding OAuth/SSO

---

## 🔧 Troubleshooting

### "Connection Refused" Error
- Check if server is running (`python main.py`)
- Verify port 8000 is not blocked by firewall
- Try accessing localhost first

### "Can't Access from Other Devices"
- Verify devices are on same WiFi
- Check Windows Firewall:
```powershell
New-NetFirewallRule -DisplayName "ChatMK" -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow
```
- Try using a tunnel service instead

### "Tunnel Disconnects"
- **Serveo:** Normal behavior, reconnect when needed
- **Cloudflare:** Check your internet connection
- **ngrok:** Verify authtoken is set correctly

### "Slow Performance"
- Reduce number of simultaneous users
- Check your internet speed (for tunnels)
- Consider hosting on a VPS for better performance

---

## 💡 Pro Tips

1. **Keep Terminal Open:** Don't close the terminal running the server or tunnel
2. **Screen/tmux:** Use for persistent sessions (Linux/macOS/Termux)
   ```bash
   screen -S chatmk
   python main.py
   # Press Ctrl+A, then D to detach
   ```
3. **Multiple Tunnels:** You can run Serveo, Cloudflare, and ngrok simultaneously
4. **Custom Branding:** Edit templates to add your logo/colors
5. **Analytics:** Monitor usage via admin dashboard at `/admin`

---

## 📞 Need Help?

1. Check the main **SETUP_GUIDE.md** for detailed instructions
2. Review the **docs/** folder for feature documentation
3. Verify you're running the latest version
4. Check if port 8000 is available

---

## 🎉 You're Ready!

Choose your sharing method and start chatting with friends, family, or colleagues from anywhere in the world!

**Local testing?** → Use localhost  
**Same room/office?** → Use local network IP  
**Quick demo?** → Use Serveo  
**Production use?** → Use Cloudflare Tunnel  
**Need debugging?** → Use ngrok

---

**Happy Chatting! 💬**