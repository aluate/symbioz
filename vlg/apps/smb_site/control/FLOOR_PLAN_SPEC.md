# Floor Plan Builder System - Technical Specification

**Purpose:** Define the modular floor plan builder system for SMB website.

---

## System Overview

An interactive drag-and-drop floor plan builder that allows clients to:
1. Start with default floor plan templates
2. Drag and drop modular rooms between floor plans
3. Build custom configurations within modular constraints
4. See real-time pricing estimates
5. Export/share floor plans

---

## Three Default Floor Plan Outlines

### 1. **Sugarline 65** - Single Module
- **Dimensions:** 16x65 feet (1,040 sq ft)
- **Description:** Basic modular unit foundation
- **Use case:** Starter home, guest house, ADU
- **Default layout:** Open concept, bedroom + bath, kitchen, living

### 2. **Twinline 130** - Two Modules Offset
- **Dimensions:** Two 16x65 modules, offset configuration (~2,080 sq ft)
- **Description:** Split floor plan with bedrooms on opposite ends, great room in middle
- **Use case:** Primary residence, family home
- **Default layout:** Master suite one end, guest bedrooms other end, central great room

### 3. **Summit Stack** - Four Modules, Two-Story
- **Dimensions:** Four modules in two-story configuration (~4,160 sq ft)
- **Description:** Staircase is a drag-drop module, allows various configurations
- **Use case:** Luxury home, large family, mountain estate
- **Default layout:** Open great room + kitchen downstairs, bedrooms + office upstairs

---

## Modular Room System

### Concept:
Rooms are **independent modules** that can be:
- Dragged between floor plans
- Copied and reused
- Sized to standard dimensions
- Validated against modular constraints

### Standard Room Sizes:
- **Kitchen:** 15x16 (240 sq ft)
- **Bedroom (Master):** 15x16 (240 sq ft)
- **Bedroom (Standard):** 12x14 (168 sq ft)
- **Bathroom (Full):** 8x10 (80 sq ft)
- **Bathroom (Half):** 6x8 (48 sq ft)
- **Living/Great Room:** Variable (based on remaining space)
- **Dining:** 12x14 (168 sq ft)
- **Office/Study:** 12x12 (144 sq ft)
- **Laundry:** 8x8 (64 sq ft)
- **Staircase Module:** 4x8 (32 sq ft) - connects two-story configurations

---

## Modular Constraints

### Physical Limits:
- **Maximum Width:** 16 feet (modular transport limit)
- **Maximum Length:** 70 feet per module
- **Maximum Height:** Two stories (requires staircase module)
- **Module Count:** Up to 4 modules per configuration

### Validation Rules:
- Rooms must fit within module boundaries
- Cannot overlap rooms
- Must maintain minimum hallway widths (4 feet)
- Staircase module required for two-story configurations
- Module connections must be valid (aligned)

---

## Builder Interface

### Components Needed:

1. **FloorPlanCanvas**
   - Drag-and-drop canvas
   - Grid overlay (optional, toggle)
   - Zoom controls
   - Pan controls

2. **RoomLibrary**
   - List of available rooms
   - Drag to add to canvas
   - Filter by category

3. **DefaultFloorPlans**
   - Three starting templates
   - One-click load
   - Can modify after loading

4. **RoomEditor**
   - Resize rooms (within constraints)
   - Rotate rooms
   - Delete rooms
   - Change room type

5. **PricingCalculator**
   - Real-time price updates
   - Base price per module
   - Room-specific pricing
   - Finish/upgrade options

6. **ConstraintValidator**
   - Validates modular constraints
   - Shows warnings/errors
   - Suggests fixes

---

## Technical Implementation

### Libraries:
- **React DnD** or **@dnd-kit** - Drag and drop
- **SVG** or **Canvas** - Floor plan rendering
- **React** - Component framework

### Data Structure:

```typescript
interface FloorPlan {
  id: string
  name: string
  modules: Module[]
  totalSqFt: number
  estimatedPrice: number
}

interface Module {
  id: string
  dimensions: { width: number; length: number }
  rooms: Room[]
  position: { x: number; y: number }
  level: 1 | 2  // floor level
}

interface Room {
  id: string
  type: RoomType
  dimensions: { width: number; length: number }
  position: { x: number; y: number }
  moduleId: string
}

type RoomType = 
  | "kitchen"
  | "bedroom-master"
  | "bedroom-standard"
  | "bathroom-full"
  | "bathroom-half"
  | "living"
  | "dining"
  | "office"
  | "laundry"
  | "staircase"
```

---

## User Flow

1. **Land on Floor Plans page**
2. **Choose starting point:**
   - Start with default template (Sugarline 65, Twinline 130, Summit Stack)
   - Or start with blank canvas
3. **Build:**
   - Drag rooms from library
   - Arrange on canvas
   - System suggests module count ("This would be 3 modules")
4. **Validate:**
   - System checks constraints
   - Shows warnings if needed
5. **Price:**
   - Real-time pricing display
   - Base + room + finishes
6. **Save/Share:**
   - Save configuration
   - Export floor plan
   - Request quote

---

## Success Criteria

- ✅ Users can drag and drop rooms
- ✅ Three default templates load correctly
- ✅ Modular constraints are enforced
- ✅ Pricing updates in real-time
- ✅ System suggests module count automatically
- ✅ Interface feels premium, not toy-like
- ✅ Works on desktop and tablet (mobile optional)

---

## Future Enhancements

- 3D preview
- Virtual walkthrough
- Photo-realistic renderings
- Integration with architectural software
- Save/share with SMB team
- Direct quote request

