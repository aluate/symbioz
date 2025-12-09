# Local Testing Guide - SMB Site

**Test your site locally before deploying!**

---

## 🚀 Quick Start (3 Steps)

### **Step 1: Install Dependencies**

Navigate to the site directory and install:

```powershell
cd "C:\Users\small\My Drive\vlg\apps\smb_site"
npm install
```

**First time?** This will install:
- Next.js 14
- React 18
- TypeScript
- Drag-and-drop libraries (@dnd-kit)
- All other dependencies

**Expected time:** 2-5 minutes

---

### **Step 2: Start Development Server**

Run the dev server:

```powershell
npm run dev
```

**You should see:**
```
- ready started server on 0.0.0.0:3000, url: http://localhost:3000
- event compiled client and server successfully
```

---

### **Step 3: Open in Browser**

Open your browser and go to:
**http://localhost:3000**

**That's it!** Your site is running locally. 🎉

---

## ✅ What to Test

### **1. Navigation**
- [ ] Click through all pages (Home, Our Homes, Floor Plans, Process, About, Contact)
- [ ] Check that all links work
- [ ] Verify mobile menu (if testing on mobile/resized window)

### **2. Floor Plan Builder** ⭐
- [ ] Load a template (Sugarline 65, Twinline 130, Summit Stack)
- [ ] Drag rooms from library to canvas
- [ ] Select a room (should highlight)
- [ ] Delete a room
- [ ] Check pricing updates in real-time
- [ ] Test zoom controls
- [ ] Toggle grid on/off

### **3. Responsive Design**
- [ ] Resize browser window
- [ ] Test on mobile/tablet view
- [ ] Check that all content is readable

### **4. Visual Check**
- [ ] Brand colors display correctly
- [ ] Fonts load properly (Playfair Display, Inter)
- [ ] Images/placeholders show
- [ ] No console errors (open DevTools: F12)

### **5. Forms**
- [ ] Contact form displays correctly
- [ ] Form validation works (if implemented)

---

## 🛠️ Troubleshooting

### **"npm: command not found"**
**Solution:** Install Node.js from https://nodejs.org/
- Download LTS version
- Install with default settings
- Restart PowerShell/terminal

### **"Port 3000 already in use"**
**Solution:** Use a different port:
```powershell
$env:PORT=3001; npm run dev
```
Then open: http://localhost:3001

### **"Module not found" errors**
**Solution:** Reinstall dependencies:
```powershell
rm -r node_modules
rm package-lock.json
npm install
```

### **TypeScript errors**
**Solution:** These are usually just warnings. The site should still run. If blocking:
```powershell
npm run build
```
This will show all errors. Most are likely minor type issues.

### **Site looks broken/styled wrong**
**Solution:** 
1. Hard refresh browser: `Ctrl + Shift + R`
2. Clear browser cache
3. Check console for CSS loading errors

---

## 📋 Available Commands

```powershell
# Start development server (with hot reload)
npm run dev

# Build for production (test production build)
npm run build

# Start production server (after building)
npm run start

# Check for linting errors
npm run lint
```

---

## 🎯 Testing Checklist

Before deploying, make sure:

- [ ] All pages load without errors
- [ ] Floor Plan Builder works (drag-and-drop, templates, pricing)
- [ ] Navigation works on all pages
- [ ] Site is responsive (mobile/tablet)
- [ ] No console errors
- [ ] Build succeeds: `npm run build`

---

## 💡 Pro Tips

1. **Keep dev server running** while making changes - it auto-reloads!
2. **Use browser DevTools** (F12) to check for errors
3. **Test the Floor Plan Builder thoroughly** - it's the main feature
4. **Try different browsers** - Chrome, Firefox, Edge
5. **Test on mobile device** - use your phone's browser on same network

---

## 🚀 Ready to Deploy?

Once local testing passes:
1. ✅ All pages work
2. ✅ Floor Plan Builder functions
3. ✅ No console errors
4. ✅ Build succeeds

**Then follow the deployment guide:**
- `START_HERE.md` - Quick deployment steps
- `STEP_BY_STEP_DEPLOY.md` - Detailed guide

---

**Happy testing!** 🎉

