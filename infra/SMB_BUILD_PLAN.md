# 🏗️ Sugar Mountain Builders - Complete Build Plan

**Date:** November 30, 2025  
**Goal:** Build complete SMB website with modular floor plan builder  
**Domain:** SugarMountainBuilders.com (currently at Wix, needs transfer to Vercel)

---

## 🎯 Project Overview

**Sugar Mountain Builders** - Luxury modular home builder targeting high-end mountain markets.

**Key Features:**
1. Premium website with luxury copy
2. Modular floor plan builder (drag-and-drop interface)
3. Three default floor plans (16x65 single, two 16x65 offset, 4-mod two-story)
4. Modular room system (drag rooms between floor plans)
5. Pricing calculator
6. Contact/inquiry system

---

## 📋 Build Phases

### **Phase 1: Project Setup & Structure**
- Generate project spec from template
- Set up Next.js frontend
- Configure Otto for SMB
- Set up GitHub repo

### **Phase 2: Brand & Copy System**
- Create SMB copy control document
- Generate all page copy (luxury tone)
- Set up brand voice guidelines
- Create copy templates

### **Phase 3: Floor Plan Builder**
- Build drag-and-drop interface
- Create modular room system
- Implement three default floor plans
- Add pricing calculation logic
- Room/module library

### **Phase 4: Website Pages**
- Home page
- Our Homes (model showcase)
- Floor Plans (interactive builder)
- Process page
- About page
- Contact page

### **Phase 5: Infrastructure**
- Provision with Otto
- Set up Vercel deployment
- Configure domain (manual step batched)
- Set up Supabase (if needed for forms)

### **Phase 6: Polish & Launch**
- Test all features
- Fix any issues
- Final validation
- Launch checklist

---

## 🎨 Brand Voice

**Luxury, Premium, Understated, Mountain-Modern**

- No casual language
- No jokes or humor
- Professional, refined
- Appeals to top-end market
- Modular framed as superior, not budget

---

## 🏗️ Floor Plan System

### **Three Default Outlines:**

1. **Sugarline 65** - 16x65 single module
   - Basic modular unit
   - Foundation for all plans

2. **Twinline 130** - Two 16x65 modules offset
   - Split floor plan
   - Bedrooms on opposite ends
   - Great room in middle

3. **Summit Stack** - Four modules, two-story
   - Staircase as drag-drop module
   - Multiple configurations possible

### **Modular Room System:**

- Rooms are independent modules
- Can drag-drop between floor plans
- Standard sizes (e.g., 15x16 kitchen)
- Validates against modular constraints

### **Features:**

- Drag-and-drop interface
- Real-time pricing
- Modular constraint validation
- 3D preview (future)
- Export floor plan (future)

---

## 📁 Project Structure

```
sugar_mountain_builders/
  apps/
    web/                    # Next.js frontend
      src/
        app/
          page.tsx          # Home
          our-homes/        # Model showcase
          floor-plans/      # Interactive builder
          process/          # Process page
          about/            # About page
          contact/          # Contact page
        components/
          FloorPlanBuilder/ # Drag-drop builder
          RoomLibrary/      # Room modules
          PricingDisplay/   # Pricing calculator
        lib/
          copy.ts           # SMB copy system
          brand.ts          # Brand voice
  control/
    SMB_COPY_CONTROL.md    # Copy generation guide
    SMB_BRAND_VOICE.md     # Brand guidelines
    FLOOR_PLAN_SPEC.md     # Floor plan system spec
  infra/
    project-spec.yaml      # Otto config
```

---

## 🚀 Implementation Order

1. ✅ Create project structure
2. ✅ Generate project spec with Otto
3. ✅ Set up brand/copy control docs
4. ✅ Build floor plan builder component
5. ✅ Create all pages
6. ✅ Generate copy for all pages
7. ✅ Provision infrastructure
8. ✅ Deploy and test

---

## 📝 Manual Steps (Batched at End)

1. Transfer domain from Wix to Vercel
2. Point DNS to Vercel
3. Test domain connection

---

**Ready to build!** 🚀

