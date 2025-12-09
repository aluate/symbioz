# One-Click Start Guide - Desktop Icon Setup

## 🚀 The "Big Red Button" Solution

You now have **one-click desktop access** to start Otto + Life OS!

---

## Quick Setup (2 minutes)

### Option 1: Simple Batch File (Recommended)

1. **Right-click** `start_otto_lifeos_mobile.bat` in your repo root
2. **Send to → Desktop (create shortcut)**
3. **Rename shortcut** to: `🚀 Start Otto + Life OS`
4. **Optional:** Right-click shortcut → Properties → Run: **Minimized**

**Done!** Double-click to start everything.

### Option 2: PowerShell Control Panel (Fancy)

1. **Right-click** `START_OTTO_LIFEOS.bat` in your repo root
2. **Send to → Desktop (create shortcut)**
3. **Rename shortcut** to: `🎛️ Otto Control Panel`

This gives you a menu:
- Start all servers
- Stop all servers
- Show IP address
- Check server status

---

## What You Get

### Files Created:

1. **`start_otto_lifeos_mobile.bat`** - Simple one-click start
2. **`stop_otto_lifeos.bat`** - Stop all servers
3. **`get_my_ip.bat`** - Show your IP address
4. **`otto_lifeos_control.ps1`** - PowerShell control panel
5. **`START_OTTO_LIFEOS.bat`** - Launcher for control panel

### Desktop Shortcuts:

- **🚀 Start Otto + Life OS** - Starts everything
- **📱 Get My IP** (optional) - Shows IP for phone access
- **🎛️ Otto Control Panel** (optional) - Menu-driven control

---

## How It Works

### When You Double-Click:

1. **Three terminal windows open:**
   - Otto API (port 8001)
   - Life OS Backend (port 8000)
   - Life OS Frontend (port 3000)

2. **All servers start automatically:**
   - Otto API accepts prompts
   - Life OS backend serves APIs
   - Life OS frontend serves web UI

3. **Ready in ~10 seconds:**
   - All servers running
   - Accessible from your network
   - Ready for phone access

### To Use from Phone:

1. **Double-click** `📱 Get My IP` (or run `ipconfig`)
2. **Copy your IP** (e.g., `192.168.1.100`)
3. **On phone:** Go to `http://YOUR_IP:3000`
4. **Start sending prompts!**

---

## Server Details

| Server | Port | Window Title | Purpose |
|--------|------|--------------|---------|
| Otto API | 8001 | Otto API - Port 8001 | Receives prompts |
| Life OS Backend | 8000 | Life OS Backend - Port 8000 | API server |
| Life OS Frontend | 3000 | Life OS Frontend - Port 3000 | Web interface |

---

## Stopping Servers

### Option 1: Close Windows
- Just close the three terminal windows

### Option 2: Stop Script
- Double-click `stop_otto_lifeos.bat`

### Option 3: Control Panel
- Use the PowerShell control panel menu

---

## Troubleshooting

**"Port already in use"?**
- Run `stop_otto_lifeos.bat` first
- Or close the terminal windows manually

**Servers won't start?**
- Check dependencies are installed:
  - `cd apps/otto && pip install -r requirements.txt`
  - `cd apps/life_os/backend && pip install -r requirements.txt`
  - `cd apps/life_os/frontend && npm install`

**Can't access from phone?**
- Make sure phone and computer are on same Wi-Fi
- Check firewall isn't blocking ports
- Verify servers are running (check terminal windows)

**Path issues?**
- The batch files use relative paths from repo root
- Make sure you're running from the repo root directory
- Or edit the batch file to use absolute paths

---

## Future: Not on Same Wi-Fi

For accessing from anywhere (not just same Wi-Fi), consider:

- **Tailscale** - Free VPN that makes devices appear on same network
- **ZeroTier** - Similar to Tailscale
- **ngrok** - Temporary tunnel (for testing)

Your current setup is perfect for these - they just make your phone think it's on the same network.

---

## What's Next?

1. **Double-click the desktop shortcut** to start
2. **Get your IP** (double-click Get My IP shortcut)
3. **Open on phone:** `http://YOUR_IP:3000`
4. **Start using Otto from anywhere on your network!**

---

**You're one double-click away from magic!** ✨🚀

