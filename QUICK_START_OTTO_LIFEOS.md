# Quick Start: Otto + Life OS - Send Prompts from Anywhere

## 🚀 Get It Running in 2 Minutes

### Step 1: Start Otto API Server

```bash
cd apps/otto
pip install -r requirements.txt
otto server
```

Otto API will be running on `http://localhost:8001`

### Step 2: Start Life OS Backend

```bash
cd apps/life_os/backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Life OS API will be running on `http://localhost:8000`

### Step 3: Start Life OS Frontend

```bash
cd apps/life_os/frontend
npm install
npm run dev
```

Life OS web interface will be on `http://localhost:3000`

## 📝 Send Prompts from Web Interface

1. Open `http://localhost:3000` in your browser
2. Type a prompt like:
   - "List the repository structure"
   - "Audit the Otto repo"
   - "Run health checks"
3. Click "Send to Otto" or press Cmd/Ctrl + Enter

## 🔌 Send Prompts via API

### From Life OS API:
```bash
curl -X POST http://localhost:8000/otto/prompt \
  -H "Content-Type: application/json" \
  -d '{"prompt": "List repository structure"}'
```

### Direct to Otto API:
```bash
curl -X POST http://localhost:8001/prompt \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Audit the Otto repository"}'
```

## 📱 Send from Anywhere

You can send prompts from:
- ✅ Web browser (Life OS interface)
- ✅ Mobile browser (if on same network)
- ✅ API clients (Postman, Insomnia, etc.)
- ✅ Other apps (via HTTP requests)
- ✅ Command line (curl, httpie, etc.)

## 🎯 What Works Now

- ✅ Text prompts via HTTP API
- ✅ Structured tasks via HTTP API
- ✅ Web interface in Life OS
- ✅ Health checks
- ✅ Repo listing
- ✅ Repo auditing

## 🔮 Coming Soon (Phase 2)

- LLM integration for natural language understanding
- Google Drive integration
- Advanced prompt routing
- Task queuing and scheduling

## 🐛 Troubleshooting

**Otto API not responding?**
- Check if it's running: `curl http://localhost:8001/health`
- Make sure port 8001 is not in use

**Life OS can't connect to Otto?**
- Verify Otto API is running on port 8001
- Check `apps/life_os/backend/api/otto.py` for the correct URL

**Frontend not loading?**
- Make sure Life OS backend is running on port 8000
- Check browser console for errors

