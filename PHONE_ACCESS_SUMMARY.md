# ✅ Yes! You Can Use Otto on Your Phone

## Quick Answer

**YES** - Otto is fully accessible from your phone! Here's how:

## Two Ways to Access

### 1. Life OS Web Interface (Easiest)

1. **Find your computer's IP address:**
   - Windows: `ipconfig` (look for IPv4 Address)
   - Mac/Linux: `ifconfig` or `ip addr show`

2. **Start servers with network access:**
   ```bash
   # Terminal 1 - Otto
   cd apps/otto
   otto server --host 0.0.0.0 --port 8001
   
   # Terminal 2 - Life OS Backend
   cd apps/life_os/backend
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   
   # Terminal 3 - Life OS Frontend
   cd apps/life_os/frontend
   npm run dev -- -H 0.0.0.0
   ```

3. **On your phone (same Wi-Fi):**
   - Open browser
   - Go to: `http://YOUR_IP:3000`
   - Start sending prompts!

### 2. Direct Otto API (Advanced)

Access Otto API directly from your phone:
- URL: `http://YOUR_IP:8001/prompt`
- Use any API client or browser

## What I Just Updated

✅ **Life OS Backend CORS** - Now allows access from anywhere (not just localhost)  
✅ **Startup Scripts** - Updated to use `0.0.0.0` for network access  
✅ **Mobile-Friendly UI** - Improved touch targets and font sizes  
✅ **New Mobile Script** - `start_dev_mobile.bat` for easy mobile access  

## Example

If your computer's IP is `192.168.1.100`:

**From your phone browser:**
- Life OS: `http://192.168.1.100:3000` ← **Use this!**
- Otto API: `http://192.168.1.100:8001`
- Life OS API: `http://192.168.1.100:8000`

## Mobile Features

The Life OS interface is now mobile-optimized:
- ✅ Larger touch targets
- ✅ Better font sizes (no zoom on iOS)
- ✅ Responsive layout
- ✅ Full-screen textarea
- ✅ Easy-to-tap buttons

## Quick Start

1. Run `apps/life_os/frontend/start_dev_mobile.bat`
2. Find your IP: `ipconfig` (Windows) or `ifconfig` (Mac/Linux)
3. On phone: `http://YOUR_IP:3000`
4. Start sending prompts!

## Troubleshooting

**Can't connect?**
- Make sure phone and computer are on same Wi-Fi
- Check firewall isn't blocking ports
- Verify servers are running with `0.0.0.0` (not `localhost`)

**See:** `ACCESS_OTTO_FROM_PHONE.md` for detailed troubleshooting

---

**You're all set! Use Otto from your phone right now.** 📱✨

