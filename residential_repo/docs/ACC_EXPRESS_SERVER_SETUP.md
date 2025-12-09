# ACC Express - Server Deployment Guide

**Purpose:** This guide explains how to deploy ACC Express as an internal web application on a Windows server machine, allowing coworkers to access it from their browsers without installing Python locally.

---

## Overview

ACC Express is a web-based cabinet ordering application that provides a guided, multi-step wizard for creating cabinet orders. This deployment guide sets up ACC Express to run on a single Windows server machine, accessible to all coworkers on the local network via their web browsers.

**Goal:** One machine runs the app 24/7; everyone else accesses it at `http://SERVER-NAME:8001/express-order` from any browser.

---

## Prerequisites on the Server Machine

Before starting, ensure the server machine has:

1. **Windows 10/11** (64-bit recommended)

2. **Python 3.11 or higher**
   - Download from [python.org](https://www.python.org/downloads/)
   - During installation, check "Add Python to PATH"
   - Verify installation:
     ```powershell
     python --version
     # or
     py --version
     ```
   - Should show Python 3.11.x or higher

3. **Network Access**
   - Server must be on the same local network as coworker machines
   - Outbound internet allowed (for initial `pip install`)

4. **OneDrive or File Access**
   - Either:
     - OneDrive synced to server with `residential_repo` folder, OR
     - Ability to copy/unzip the repo from a shared location

---

## Getting the Code onto the Server

### Option A: OneDrive Sync (Recommended)

If the `residential_repo` folder is in OneDrive:

1. On the server machine, ensure OneDrive is installed and synced
2. Navigate to the OneDrive folder containing `residential_repo`
3. Verify the folder structure:
   ```
   residential_repo/
   ├── apps/
   ├── config/
   ├── docs/
   ├── tests/
   └── ...
   ```

### Option B: Manual Copy/Unzip

If OneDrive sync is not available:

1. On your development machine, zip the entire `residential_repo` folder
2. Copy the zip file to the server (via network share, USB drive, etc.)
3. Unzip to a location like `C:\acc_express` (or any path you prefer)
4. Verify the folder structure matches the above

**Note:** The exact path doesn't matter, but remember it for the next steps.

---

## Creating and Using a Virtual Environment

A virtual environment isolates ACC Express dependencies from other Python projects.

1. **Open PowerShell** in the repo root folder (where `apps/`, `config/`, etc. are located)

2. **Create the virtual environment:**
   ```powershell
   py -m venv .venv
   ```

3. **Activate the virtual environment:**
   ```powershell
   .\.venv\Scripts\activate
   ```
   You should see `(.venv)` appear in your prompt.

4. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```
   This will install FastAPI, Uvicorn, Pydantic, and other required packages.

5. **Verify installation:**
   ```powershell
   pip list
   ```
   You should see `fastapi`, `uvicorn`, `pydantic` in the list.

---

## Running ACC Express on the Server

### Manual Start (For Testing)

1. **Open PowerShell** in the repo root folder

2. **Activate the virtual environment:**
   ```powershell
   .\.venv\Scripts\activate
   ```

3. **Start the server:**
   ```powershell
   uvicorn apps.web.prime_order_api:app --host 0.0.0.0 --port 8001
   ```

4. **Verify it's running:**
   - On the server machine, open a browser and go to:
     ```
     http://localhost:8001/express-order
     ```
   - You should see the ACC Express Order form

5. **Test from another machine:**
   - Find the server's IP address or hostname (see "Finding Server Address" below)
   - From a coworker's machine, open a browser and go to:
     ```
     http://SERVER-NAME:8001/express-order
     # or
     http://192.168.1.50:8001/express-order
     ```
   - You should see the same ACC Express Order form

**Important Notes:**
- `--host 0.0.0.0` makes the server accessible from other machines on the network
- `--port 8001` is the port number (can be changed if needed)
- The server will run until you press `Ctrl+C` in the PowerShell window

### Using the Server Start Script

For convenience, use the provided batch file:

1. **Double-click `start_acc_express_server.bat`** in the repo root folder

   OR

2. **Run from PowerShell:**
   ```powershell
   .\start_acc_express_server.bat
   ```

This script automatically activates the virtual environment and starts the server with the correct settings.

---

## Windows Firewall Configuration

The server must allow inbound traffic on port 8001 for other machines to connect.

### Option 1: Windows Defender Firewall (GUI)

1. Open **Control Panel** → **Windows Defender Firewall**
2. Click **Advanced settings**
3. Click **Inbound Rules** → **New Rule**
4. Select **Port** → **Next**
5. Select **TCP** and enter port **8001** → **Next**
6. Select **Allow the connection** → **Next**
7. Check all profiles (Domain, Private, Public) → **Next**
8. Name it "ACC Express Server" → **Finish**

### Option 2: PowerShell (Run as Administrator)

```powershell
New-NetFirewallRule -DisplayName "ACC Express Server" -Direction Inbound -LocalPort 8001 -Protocol TCP -Action Allow
```

### Finding the Server's IP Address or Hostname

**To find the server's IP address:**

1. Open PowerShell on the server
2. Run:
   ```powershell
   ipconfig
   ```
3. Look for **IPv4 Address** under your active network adapter (usually something like `192.168.1.50`)

**To find the server's hostname:**

1. Open PowerShell on the server
2. Run:
   ```powershell
   hostname
   ```
3. The output is the hostname (e.g., `ACC-SERVER` or `DESKTOP-ABC123`)

**Coworkers will use:**
- `http://SERVER-HOSTNAME:8001/express-order` (if hostname resolution works on your network)
- OR `http://SERVER-IP:8001/express-order` (always works)

---

## Setting Up "Start on Boot" (Scheduled Task)

To make ACC Express start automatically when the server boots:

1. **Open Task Scheduler** (search "Task Scheduler" in Start menu)

2. **Create Basic Task:**
   - Click **Create Basic Task** in the right panel
   - Name: "ACC Express Server"
   - Description: "Start ACC Express web server on boot"
   - Trigger: **When the computer starts** (or **When I log on**)
   - Action: **Start a program**

3. **Configure the program:**
   - Program/script: Full path to `start_acc_express_server.bat`
     - Example: `C:\acc_express\start_acc_express_server.bat`
   - Start in: The folder containing the batch file
     - Example: `C:\acc_express`

4. **Advanced settings (optional):**
   - Check **Run whether user is logged on or not** (if you want it to run without a user logged in)
   - Check **Run with highest privileges** (may be needed depending on firewall settings)

5. **Test the task:**
   - Right-click the task → **Run**
   - Verify ACC Express starts and is accessible

**Note:** If the task runs a batch file that opens a window, you may want to configure it to run hidden or redirect output to a log file.

---

## How Coworkers Connect

Once the server is running, coworkers can access ACC Express from any machine on the same network:

1. **Open a web browser** (Chrome, Edge, Firefox, etc.)

2. **Navigate to:**
   ```
   http://SERVER-NAME:8001/express-order
   ```
   OR
   ```
   http://SERVER-IP:8001/express-order
   ```

3. **No installation required** — they just need a browser

**Example URLs:**
- `http://ACC-SERVER:8001/express-order`
- `http://192.168.1.50:8001/express-order`
- `http://DESKTOP-ABC123:8001/express-order`

---

## Troubleshooting

### Can't Connect from Another Machine

**Check 1: Server is running**
- On the server, verify the PowerShell window shows "Uvicorn running on..."
- Try accessing `http://localhost:8001/express-order` on the server itself

**Check 2: Firewall**
- Ensure Windows Firewall allows inbound traffic on port 8001 (see "Windows Firewall Configuration" above)
- Temporarily disable firewall as a test (if it works, firewall is the issue)

**Check 3: Network connectivity**
- Ensure both machines are on the same network
- Try pinging the server from the coworker's machine:
  ```powershell
  ping SERVER-NAME
  # or
  ping SERVER-IP
  ```

**Check 4: Correct URL**
- Use `http://` not `https://`
- Include the port number `:8001`
- Use the full path `/express-order`

**Check 5: Host binding**
- Ensure the server was started with `--host 0.0.0.0` (not `localhost` or `127.0.0.1`)
- The `start_acc_express_server.bat` script includes this automatically

### App Not Starting

**Check 1: Python version**
```powershell
python --version
```
Should be 3.11 or higher.

**Check 2: Virtual environment**
- Ensure `.venv` folder exists in the repo root
- Activate it: `.\.venv\Scripts\activate`

**Check 3: Dependencies**
```powershell
pip install -r requirements.txt
```

**Check 4: Port in use**
- Another application might be using port 8001
- Change the port in `start_acc_express_server.bat`:
  ```
  uvicorn apps.web.prime_order_api:app --host 0.0.0.0 --port 8002
  ```
- Update firewall rules and URLs accordingly

**Check 5: Error messages**
- Look at the PowerShell output for error messages
- Common issues:
  - Missing dependencies → run `pip install -r requirements.txt`
  - Path issues → ensure you're in the repo root folder
  - Import errors → check that `apps/web/prime_order_api.py` exists

### Logs and Debugging

**Uvicorn logs:**
- The PowerShell window running the server shows all requests and errors
- Watch this window for debugging information

**Common log messages:**
- `INFO:     Uvicorn running on http://0.0.0.0:8001` → Server started successfully
- `ERROR:    [Errno 10048] Only one usage of each socket address` → Port 8001 is already in use
- `ModuleNotFoundError` → Missing dependency, run `pip install -r requirements.txt`

---

## Updating ACC Express

When updates are made to the code:

1. **On the server**, stop the running server (`Ctrl+C` in the PowerShell window)

2. **Update the code:**
   - If using OneDrive: wait for sync to complete
   - If using manual copy: copy the updated files

3. **Restart the server:**
   - Run `start_acc_express_server.bat` again
   - Or restart the Scheduled Task

4. **Verify:**
   - Check that the new version is accessible
   - Test a quick order submission

---

## Security Notes

**Current State:**
- ACC Express has no authentication (anyone with the URL can access it)
- This is acceptable for internal-only use on a trusted network
- Do NOT expose this to the internet without adding authentication

**Recommendations:**
- Keep the server on a private network (not directly internet-facing)
- Consider adding a simple login page in future updates
- Monitor usage if needed

---

## Support

If you encounter issues not covered in this guide:

1. Check the Uvicorn logs in the PowerShell window
2. Review `docs/acc_express_project_report.md` for technical details
3. Verify all prerequisites are met
4. Test with `http://localhost:8001/express-order` on the server first

---

**Last Updated:** 2024-12-19

