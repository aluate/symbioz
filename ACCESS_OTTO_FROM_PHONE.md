# Access Otto from Your Phone

**Yes! You can use Otto on your phone to submit prompts.**

## Quick Setup (2 minutes)

### Step 1: Find Your Computer's IP Address

**Windows:**
```bash
ipconfig
```
Look for "IPv4 Address" under your active network adapter (usually starts with 192.168.x.x or 10.x.x.x)

**Mac/Linux:**
```bash
ifconfig
# or
ip addr show
```

### Step 2: Start the Servers

Make sure both servers are running:

**Terminal 1 - Otto API:**
```bash
cd apps/otto
otto server --host 0.0.0.0 --port 8001
```

**Terminal 2 - Life OS Backend:**
```bash
cd apps/life_os/backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 3 - Life OS Frontend:**
```bash
cd apps/life_os/frontend
npm run dev -- -H 0.0.0.0
```

**Important:** Use `0.0.0.0` instead of `localhost` so the servers accept connections from your network.

### Step 3: Access from Your Phone

1. **Make sure your phone is on the same Wi-Fi network** as your computer
2. **Open your phone's browser**
3. **Go to:** `http://YOUR_IP_ADDRESS:3000`

For example, if your IP is `192.168.1.100`:
- Life OS Interface: `http://192.168.1.100:3000`
- Otto API Direct: `http://192.168.1.100:8001`

## Using the Life OS Interface

The Life OS web interface works great on mobile:
- Type your prompt in the text area
- Tap "Send to Otto" or use keyboard shortcuts
- See results instantly

## Direct API Access (Advanced)

You can also send prompts directly to Otto API from your phone using:
- Browser (for testing)
- API client apps (like Postman mobile)
- Shortcuts/Siri Shortcuts (iOS)
- Tasker (Android)

**Example curl from phone:**
```bash
curl -X POST http://192.168.1.100:8001/prompt \
  -H "Content-Type: application/json" \
  -d '{"prompt": "List repository structure"}'
```

## Troubleshooting

**Can't connect?**
1. Check that phone and computer are on same Wi-Fi
2. Verify firewall isn't blocking ports 3000, 8000, 8001
3. Try pinging your computer's IP from phone
4. Make sure servers are running with `0.0.0.0` not `localhost`

**Firewall Issues (Windows):**
- Windows Firewall may block incoming connections
- Allow Python/Node through firewall when prompted
- Or temporarily disable firewall for testing

**Firewall Issues (Mac):**
- System Preferences → Security & Privacy → Firewall
- Allow Python/Node through firewall

## Making It Permanent

For easier access, you can:
1. **Bookmark the Life OS URL** on your phone
2. **Add to home screen** (iOS/Android) for app-like experience
3. **Set up a static IP** for your computer so the address doesn't change
4. **Use a service like ngrok** for external access (not recommended for production)

## Security Note

⚠️ **Important:** The current setup allows access from any device on your local network. This is fine for home use, but:
- Don't expose these ports to the internet
- Consider adding authentication for production use
- Use HTTPS in production

## Quick Reference

**Life OS Web Interface:**
- URL: `http://YOUR_IP:3000`
- Best for: Easy prompt submission from phone

**Otto API Direct:**
- URL: `http://YOUR_IP:8001`
- Best for: Programmatic access, automation

**Life OS Backend:**
- URL: `http://YOUR_IP:8000`
- Best for: API access to Life OS features

---

**You're all set! Use Otto from anywhere on your network.** 📱

