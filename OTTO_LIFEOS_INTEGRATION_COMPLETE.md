# ✅ Otto + Life OS Integration - COMPLETE

**Date:** December 2, 2025  
**Status:** ✅ READY TO USE - Send prompts from anywhere!

## 🎉 What's Been Built

### 1. Otto HTTP API Server ✅
- **File:** `apps/otto/otto/api.py`
- **Port:** 8001 (default)
- **Features:**
  - Accepts text prompts via POST `/prompt`
  - Accepts structured tasks via POST `/task`
  - Lists available skills via GET `/skills`
  - Health check via GET `/health`
  - CORS enabled (accessible from anywhere)

### 2. Life OS Backend Integration ✅
- **File:** `apps/life_os/backend/api/otto.py`
- **Port:** 8000 (default)
- **Features:**
  - Proxy endpoints to Otto API
  - `/otto/prompt` - Send prompts to Otto
  - `/otto/task` - Send structured tasks
  - `/otto/skills` - List Otto skills
  - `/otto/health` - Check Otto connection

### 3. Life OS Web Interface ✅
- **File:** `apps/life_os/frontend/app/page.tsx`
- **Port:** 3000 (default)
- **Features:**
  - Simple, clean prompt interface
  - Real-time results display
  - Error handling
  - Keyboard shortcuts (Cmd/Ctrl + Enter)
  - Otto health check button

## 🚀 Quick Start

### Option 1: Use the Batch Files (Windows)

1. **Start Otto API:**
   ```bash
   apps/otto/start_server.bat
   ```

2. **Start Life OS Backend:**
   ```bash
   apps/life_os/backend/start_server.bat
   ```

3. **Start Life OS Frontend:**
   ```bash
   apps/life_os/frontend/start_dev.bat
   ```

4. **Open Browser:**
   - Go to `http://localhost:3000`
   - Start sending prompts!

### Option 2: Manual Start

1. **Terminal 1 - Otto API:**
   ```bash
   cd apps/otto
   pip install -r requirements.txt
   otto server
   ```

2. **Terminal 2 - Life OS Backend:**
   ```bash
   cd apps/life_os/backend
   pip install -r requirements.txt
   uvicorn main:app --reload --port 8000
   ```

3. **Terminal 3 - Life OS Frontend:**
   ```bash
   cd apps/life_os/frontend
   npm install
   npm run dev
   ```

## 📝 How to Use

### From Web Interface (Easiest)

1. Open `http://localhost:3000`
2. Type your prompt in the text area
3. Click "Send to Otto" or press Cmd/Ctrl + Enter
4. See results instantly!

**Example Prompts:**
- "List the repository structure"
- "Audit the Otto repo"
- "Run health checks"

### From API (Programmatic)

**Via Life OS API:**
```bash
curl -X POST http://localhost:8000/otto/prompt \
  -H "Content-Type: application/json" \
  -d '{"prompt": "List repository structure"}'
```

**Direct to Otto API:**
```bash
curl -X POST http://localhost:8001/prompt \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Audit the Otto repository"}'
```

**Structured Task:**
```bash
curl -X POST http://localhost:8001/task \
  -H "Content-Type: application/json" \
  -d '{
    "type": "repo_list",
    "payload": {
      "target_repo": ".",
      "output_path": "reports/tree.md"
    }
  }'
```

## 🌐 Access from Anywhere

### Same Network (Mobile/Other Devices)

1. Find your computer's IP address:
   ```bash
   # Windows
   ipconfig
   
   # Mac/Linux
   ifconfig
   ```

2. Access from mobile/other device:
   - `http://YOUR_IP:3000` (Life OS web interface)
   - `http://YOUR_IP:8001` (Otto API directly)

### From Other Apps

Any app that can make HTTP requests can send prompts:
- Postman
- Insomnia
- Python scripts
- JavaScript/TypeScript
- Mobile apps
- Browser extensions
- etc.

## 📋 API Endpoints Reference

### Otto API (Port 8001)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API info |
| GET | `/health` | Health check |
| GET | `/skills` | List available skills |
| POST | `/prompt` | Send text prompt |
| POST | `/task` | Send structured task |

### Life OS API (Port 8000)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API info |
| GET | `/health` | Health check |
| GET | `/otto/health` | Check Otto connection |
| GET | `/otto/skills` | List Otto skills |
| POST | `/otto/prompt` | Send prompt to Otto |
| POST | `/otto/task` | Send task to Otto |

## 🔧 Configuration

### Otto API Port
Edit `apps/otto/otto/cli.py` or use:
```bash
otto server --port 8001
```

### Life OS Backend Port
Edit `apps/life_os/backend/start_server.bat` or use:
```bash
uvicorn main:app --reload --port 8000
```

### Life OS Frontend Port
Edit `apps/life_os/frontend/package.json` or use:
```bash
npm run dev -- -p 3000
```

## 🎯 What Works Now

✅ Text prompts via HTTP  
✅ Structured tasks via HTTP  
✅ Web interface  
✅ Mobile access (same network)  
✅ API access from any client  
✅ Health checks  
✅ Error handling  
✅ CORS enabled  

## 🔮 Coming Next (Phase 2)

- LLM integration for natural language understanding
- Advanced prompt routing
- Task queuing
- Google Drive integration
- Scheduled tasks
- More skills

## 🐛 Troubleshooting

**"Could not connect to Otto API"**
- Make sure Otto server is running: `curl http://localhost:8001/health`
- Check if port 8001 is available

**"Frontend not loading"**
- Make sure Life OS backend is running on port 8000
- Check browser console for errors

**"Import errors"**
- Make sure all dependencies are installed:
  - `pip install -r apps/otto/requirements.txt`
  - `pip install -r apps/life_os/backend/requirements.txt`
  - `npm install` in `apps/life_os/frontend`

## 📁 Files Created/Modified

### New Files:
- `apps/otto/otto/api.py` - HTTP API server
- `apps/life_os/backend/api/otto.py` - Otto integration
- `apps/life_os/backend/api/__init__.py` - API module init
- `apps/life_os/frontend/app/page.tsx` - Web interface
- `apps/life_os/frontend/app/layout.tsx` - Layout
- `apps/otto/start_server.bat` - Startup script
- `apps/life_os/backend/start_server.bat` - Startup script
- `apps/life_os/frontend/start_dev.bat` - Startup script
- `QUICK_START_OTTO_LIFEOS.md` - Quick start guide

### Modified Files:
- `apps/otto/otto/cli.py` - Added server command
- `apps/otto/requirements.txt` - Added FastAPI/uvicorn
- `apps/life_os/backend/main.py` - Added Otto router
- `apps/life_os/backend/requirements.txt` - Added httpx
- `apps/otto/README.md` - Updated with API info

## ✨ You're Ready!

Everything is set up and ready to use. You can now send prompts to Otto from:
- ✅ Web browser
- ✅ Mobile browser
- ✅ API clients
- ✅ Other applications
- ✅ Command line
- ✅ Anywhere that can make HTTP requests!

**Start the servers and start sending prompts!** 🚀

