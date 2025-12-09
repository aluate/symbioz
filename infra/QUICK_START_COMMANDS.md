# Quick Start Commands - Copy & Paste

## ✅ Dependencies Installed!

All Otto dependencies are now installed. Here are the commands you'll need:

---

## 📋 Step-by-Step Commands

### 1. Validate Configuration Files

```powershell
python infra/validate_configs.py
```

**Status:** ✅ All config files are valid! Just need to fill in 3 TODO placeholders.

---

### 2. Test Otto CLI

```powershell
python tools/infra.py --help
```

**Status:** ✅ CLI is working! Shows all available commands.

---

### 3. Run Dry-Run Diagnostics (Safe Test)

```powershell
python tools/infra.py diag --env=prod --dry-run
```

**What it does:** Tests Otto without making any changes. Generates reports in `diagnostics/` folder.

**Status:** ⚠️ Will work after you fill in TODO placeholders in config files.

---

### 4. Run Dry-Run Provisioning (Safe Test)

```powershell
python tools/infra.py provision-project --spec infra/project-specs/catered-by-me.yaml --env=prod --dry-run
```

**What it does:** Shows what Otto would do to provision your infrastructure (without actually doing it).

**Status:** ⚠️ Will work after you fill in TODO placeholders and set environment variables.

---

### 5. Run Dry-Run Deployment (Safe Test)

```powershell
python tools/infra.py deploy --spec infra/project-specs/catered-by-me.yaml --env=prod --dry-run
```

**What it does:** Shows what Otto would do to deploy your app (without actually deploying).

**Status:** ⚠️ Will work after you fill in TODO placeholders and set environment variables.

---

## 🔑 Before Running Real Commands

You still need to:

1. **Fill in TODO placeholders** (see `infra/FINDING_YOUR_KEYS_AND_IDS.md`):
   - `infra/providers/render.yaml` - Render service ID
   - `infra/providers/supabase.yaml` - Supabase project ref
   - `infra/providers/stripe.yaml` - Stripe webhook ID

2. **Set environment variables** (create `.env` file):
   - Copy `infra/.env.example` to `.env`
   - Fill in your API keys (see `infra/FINDING_YOUR_KEYS_AND_IDS.md`)

---

## 🎯 Next Steps

1. ✅ Dependencies installed (DONE!)
2. ✅ Config validation working (DONE!)
3. ⏳ Fill in TODO placeholders
4. ⏳ Create `.env` file with your keys
5. ⏳ Test dry-run commands
6. ⏳ Run real diagnostics
7. ⏳ Deploy catered-by-me!

---

## 📖 Need Help?

- **Where to find keys/IDs:** See `infra/FINDING_YOUR_KEYS_AND_IDS.md`
- **Step-by-step guide:** See `infra/SETUP_CHECKLIST.md`
- **What I can/can't do:** See `infra/OTTO_CAN_DO_SUMMARY.md`

