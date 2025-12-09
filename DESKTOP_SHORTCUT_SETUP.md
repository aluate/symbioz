# Desktop Shortcut Setup - One-Click Start

## Quick Setup (2 minutes)

### Step 1: Create Desktop Shortcut

1. **Navigate to your repo root** (where `start_otto_lifeos_mobile.bat` is located)

2. **Right-click** `start_otto_lifeos_mobile.bat`

3. **Choose:** Send to → Desktop (create shortcut)

4. **Rename the shortcut** on your desktop to:
   - `🚀 Start Otto + Life OS`

5. **Optional - Run Minimized:**
   - Right-click the shortcut → **Properties**
   - In **Run:** dropdown, choose **Minimized**
   - Click **OK**

### Step 2: Optional - Get IP Address Shortcut

1. **Right-click** `get_my_ip.bat`
2. **Send to → Desktop (create shortcut)**
3. **Rename to:** `📱 Get My IP`

Now you have:
- **🚀 Start Otto + Life OS** - Starts all servers
- **📱 Get My IP** - Shows your IP address for phone access

## Using It

### To Start Everything:
1. **Double-click** `🚀 Start Otto + Life OS` on your desktop
2. Three terminal windows will open (one for each server)
3. Wait ~10 seconds for everything to start

### To Get Your IP:
1. **Double-click** `📱 Get My IP`
2. Copy the IP address shown
3. Use it on your phone: `http://YOUR_IP:3000`

### To Stop Everything:
1. **Double-click** `stop_otto_lifeos.bat` (or close the terminal windows)

## What Gets Started

1. **Otto API** - Port 8001
   - Window title: "Otto API - Port 8001"
   - Accepts prompts from anywhere

2. **Life OS Backend** - Port 8000
   - Window title: "Life OS Backend - Port 8000"
   - API for Life OS features

3. **Life OS Frontend** - Port 3000
   - Window title: "Life OS Frontend - Port 3000"
   - Web interface for Otto prompts

## Troubleshooting

**Servers won't start?**
- Make sure you've installed dependencies:
  - `cd apps/otto && pip install -r requirements.txt`
  - `cd apps/life_os/backend && pip install -r requirements.txt`
  - `cd apps/life_os/frontend && npm install`

**Port already in use?**
- Run `stop_otto_lifeos.bat` first
- Or close the terminal windows manually

**Can't find IP?**
- Make sure you're connected to Wi-Fi
- Run `ipconfig` manually in PowerShell

## Advanced: PowerShell Control Panel (Future)

For a fancier setup, we could create a PowerShell script with a menu:
- `1` = Start all servers
- `2` = Stop all servers
- `3` = Show IP address
- `4` = Check server status

Let me know if you want this!

---

**You're all set! Just double-click the desktop icon to start everything.** 🚀

