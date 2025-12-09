# Quick Phone Access Guide

## Start Servers for Phone Access

### Option 1: Use Updated Batch Files

1. **Start Otto:**
   ```bash
   apps/otto/start_server.bat
   ```
   (Already configured for network access)

2. **Start Life OS Backend:**
   ```bash
   apps/life_os/backend/start_server.bat
   ```
   (Now uses 0.0.0.0 for network access)

3. **Start Life OS Frontend (Mobile):**
   ```bash
   apps/life_os/frontend/start_dev_mobile.bat
   ```
   (New script for mobile access)

### Option 2: Manual Commands

**Otto API:**
```bash
cd apps/otto
otto server --host 0.0.0.0 --port 8001
```

**Life OS Backend:**
```bash
cd apps/life_os/backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Life OS Frontend:**
```bash
cd apps/life_os/frontend
npm run dev -- -H 0.0.0.0
```

## Find Your IP Address

**Windows:**
```bash
ipconfig
```
Look for "IPv4 Address" (usually 192.168.x.x)

## Access from Phone

1. Make sure phone is on same Wi-Fi
2. Open browser on phone
3. Go to: `http://YOUR_IP:3000`
4. Start sending prompts to Otto!

## Example

If your IP is `192.168.1.100`:
- Life OS: `http://192.168.1.100:3000`
- Otto API: `http://192.168.1.100:8001`
- Life OS API: `http://192.168.1.100:8000`

