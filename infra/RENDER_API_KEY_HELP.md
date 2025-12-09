# Render API Key - Important!

## 🔐 Security Feature

Render **only shows the full API key once** when you create it. After that, it's masked for security (like `rnd_KqQT3B…`).

This is **normal and expected behavior**!

---

## ✅ If You Already Copied It

If you copied the full key when you created it, use that! The full key should look like:
```
rnd_KqQT3Bxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**Just paste the full key into your `.env` file.**

---

## ⚠️ If You Didn't Save It

If you can't see the full key and didn't save it, you'll need to:

### Option 1: Create a New API Key (Recommended)

1. Go to https://dashboard.render.com
2. Click your **profile icon** (top right) → **"Account Settings"**
3. Scroll to **"API Keys"** section
4. Click **"Create API Key"**
5. Give it a name: "Otto SRE Bot" (or whatever you like)
6. **IMPORTANT:** Copy the full key immediately! It will look like:
   ```
   rnd_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```
7. Paste it into a text file or directly into your `.env` file
8. Click **"Create"**

**⚠️ WARNING:** You can only see the full key once! Copy it immediately or you'll need to create another one.

---

## 📝 Adding to Your .env File

Once you have the full key, add it to your `.env` file:

```env
RENDER_API_KEY=rnd_KqQT3Bxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Replace `rnd_KqQT3Bxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` with your **complete** key.

---

## ✅ Verify It's Correct

The Render API key should:
- Start with `rnd_`
- Be about 40-50 characters long (including the `rnd_` prefix)
- Be all lowercase letters and numbers after `rnd_`

Example format: `rnd_kqqt3b1234567890abcdefghijklmnopqrstuvwxyz`

---

## 🔄 Multiple Keys Are Fine

You can have multiple API keys. If you create a new one for Otto, you can:
- Delete the old one (if you're not using it)
- Or keep both (Render allows multiple keys)

**Recommendation:** Create a new one specifically for Otto so you can revoke it independently if needed.

---

## 🚨 Security Reminder

- ✅ Keep your API key secret
- ✅ Never commit `.env` to git (it's already in `.gitignore`)
- ✅ Never share your API key publicly
- ✅ You can revoke/delete keys anytime from Render dashboard

---

**Need help?** Let me know if you have the full key or need to create a new one!

