# Cursor Build Prompt: Complete SMB Website with Floor Plan Builder

**Context:** You're building the complete Sugar Mountain Builders website with an interactive modular floor plan builder. This is a luxury homebuilder targeting high-end mountain markets.

---

## 📋 What Already Exists

- ✅ Basic Next.js site structure at `vlg/apps/smb_site/`
- ✅ All pages (Home, Our Homes, Process, About, Contact)
- ✅ Brand colors, typography, components
- ✅ Basic content (needs luxury upgrade)

**What's Missing:**
- ❌ Floor plan builder (THE KEY FEATURE)
- ❌ Premium luxury copy (needs upgrade)
- ❌ Three default floor plans
- ❌ Modular room system
- ❌ Pricing calculator

---

## 🎯 Your Tasks

### **Task 1: Create Brand Voice & Copy Control System**

1. Create `control/SMB_COPY_CONTROL.md` (DONE - see file)
2. Create `control/SMB_BRAND_VOICE.md` (quick reference)
3. Create `lib/copy.ts` - Copy generation utilities
4. Create `lib/brand.ts` - Brand constants

### **Task 2: Build Floor Plan Builder Component**

Create interactive drag-and-drop floor plan builder:

**Components needed:**
1. `components/FloorPlanBuilder/FloorPlanCanvas.tsx` - Main canvas
2. `components/FloorPlanBuilder/RoomLibrary.tsx` - Available rooms sidebar
3. `components/FloorPlanBuilder/DefaultFloorPlans.tsx` - Template selector
4. `components/FloorPlanBuilder/PricingDisplay.tsx` - Real-time pricing
5. `components/FloorPlanBuilder/ConstraintValidator.tsx` - Validation logic
6. `lib/floorPlans.ts` - Floor plan data structures and logic
7. `lib/modularConstraints.ts` - Constraint validation

**Libraries to use:**
- `@dnd-kit/core` + `@dnd-kit/sortable` - Drag and drop
- `react-svg` or Canvas API - Floor plan rendering
- `zustand` or React Context - State management

### **Task 3: Create Three Default Floor Plans**

Create data files for three templates:
1. **Sugarline 65** - 16x65 single module
2. **Twinline 130** - Two 16x65 modules offset  
3. **Summit Stack** - Four modules, two-story

Each should include:
- Module dimensions
- Room layout
- Default room positions
- Estimated base price

### **Task 4: Generate Premium Copy**

Using `control/SMB_COPY_CONTROL.md`:
- Upgrade all existing copy to luxury tone
- Generate new copy for Floor Plans page
- Ensure consistent voice across all pages

### **Task 5: Create Floor Plans Page**

New page: `app/floor-plans/page.tsx`
- Introduction to builder
- Default floor plan showcase
- Interactive builder component
- Pricing information

### **Task 6: Update Navigation**

Add "Floor Plans" to navigation menu

---

## 🎨 Brand Requirements

**Voice:** Premium, luxury, understated, mountain-modern

**Colors:**
- Tiffany Blue: `#81D8D0`
- Black: `#000000`
- Warm White: `#F5F5F5`
- Charcoal: `#1E1E1E`

**Typography:**
- Playfair Display (headings)
- Inter (body)

**Tone:**
- NO casual language
- NO jokes or humor
- Professional, refined
- Appeals to top-end market
- Modular = superior, not budget

---

## 🏗️ Floor Plan System Requirements

### **Three Default Outlines:**
1. **Sugarline 65** - 16x65 single module (1,040 sq ft)
2. **Twinline 130** - Two 16x65 modules offset (~2,080 sq ft)
3. **Summit Stack** - Four modules, two-story (~4,160 sq ft)

### **Modular Room System:**
- Standard room sizes (15x16 kitchen, 12x14 bedroom, etc.)
- Drag-and-drop between floor plans
- Modular constraints (max 16ft width, max 70ft length)
- Real-time pricing calculation

### **Builder Features:**
- Drag rooms from library
- Resize within constraints
- Module count auto-suggestion
- Constraint validation
- Real-time pricing
- Save/share functionality

---

## 📁 File Structure

```
vlg/apps/smb_site/
  app/
    floor-plans/
      page.tsx                    # NEW: Floor Plans page
    components/
      FloorPlanBuilder/           # NEW: Builder components
        FloorPlanCanvas.tsx
        RoomLibrary.tsx
        DefaultFloorPlans.tsx
        PricingDisplay.tsx
        ConstraintValidator.tsx
  lib/
    copy.ts                       # NEW: Copy generation
    brand.ts                      # NEW: Brand constants
    floorPlans.ts                 # NEW: Floor plan logic
    modularConstraints.ts         # NEW: Constraint validation
  control/
    SMB_COPY_CONTROL.md          # DONE: Copy guide
    FLOOR_PLAN_SPEC.md           # DONE: Technical spec
    SMB_BRAND_VOICE.md           # NEW: Quick reference
```

---

## ✅ Implementation Order

1. ✅ Create control documents
2. Build floor plan data structures
3. Build RoomLibrary component
4. Build FloorPlanCanvas component
5. Build DefaultFloorPlans selector
6. Build PricingDisplay component
7. Build ConstraintValidator
8. Create Floor Plans page
9. Generate premium copy for all pages
10. Test and polish

---

## 🚀 Success Criteria

- ✅ Users can drag rooms onto canvas
- ✅ Three default templates load correctly
- ✅ Modular constraints are enforced
- ✅ Pricing updates in real-time
- ✅ Copy matches luxury brand voice
- ✅ All pages updated with premium copy
- ✅ Floor Plans page fully functional

---

## 📝 Notes

- Follow existing code patterns in the repo
- Use TypeScript throughout
- Match existing component styling
- Ensure responsive design
- Test on desktop and tablet

**Begin implementation!**

