# Setup Instructions

## First Time Setup

Before using `start_otto_lifeos_mobile.bat`, you need to install dependencies:

### Option 1: Automatic Setup (Recommended)

1. **Double-click** `setup_otto_lifeos.bat`
2. Wait for all dependencies to install
3. Done!

### Option 2: Manual Setup

**Install Otto dependencies:**
```bash
cd apps/otto
pip install -r requirements.txt
```

**Install Life OS Backend dependencies:**
```bash
cd apps/life_os/backend
pip install -r requirements.txt
```

**Install Life OS Frontend dependencies:**
```bash
cd apps/life_os/frontend
npm install
```

## After Setup

Once dependencies are installed, you can use:
- `start_otto_lifeos_mobile.bat` - Start all servers
- `stop_otto_lifeos.bat` - Stop all servers
- `get_my_ip.bat` - Get your IP address

## Troubleshooting

**"next is not recognized"**
- Run `setup_otto_lifeos.bat` first
- Or manually: `cd apps/life_os/frontend && npm install`

**"python is not recognized"**
- Make sure Python is installed and in your PATH
- Try `py` instead of `python` on Windows

**"npm is not recognized"**
- Install Node.js from https://nodejs.org/
- Restart your terminal after installation

**"uvicorn is not recognized"**
- Run `setup_otto_lifeos.bat` first
- Or manually: `pip install uvicorn fastapi`

