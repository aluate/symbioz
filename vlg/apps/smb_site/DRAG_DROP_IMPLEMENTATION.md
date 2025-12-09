# Drag and Drop Implementation Guide

## How Drag and Drop Works

### 1. Drag Tracking Flow

```
User starts drag → DragStartEvent → setActiveId
     ↓
User drags → DragOverEvent → track delta → setDragDelta
     ↓
User drops → DragEndEvent → calculate new position → update state
```

### 2. Position Calculation

```typescript
// Step 1: Track delta during drag (in DragOverEvent)
if (event.delta) {
  setDragDelta({ x: event.delta.x, y: event.delta.y })
}

// Step 2: Use delta to calculate position (in DragEndEvent)
if (dragDelta) {
  const SCALE = 4 // 1 foot = 4 pixels
  const feetOffsetX = dragDelta.x / SCALE
  const feetOffsetY = dragDelta.y / SCALE
  newPosition = {
    x: draggedRoom.position.x + feetOffsetX,
    y: draggedRoom.position.y + feetOffsetY,
  }
}

// Step 3: Snap to grid and clamp to bounds
newPosition = snapToGrid(newPosition, 4) // 4-foot grid
newPosition = {
  x: Math.max(0, Math.min(newPosition.x, moduleWidth - roomWidth)),
  y: Math.max(0, Math.min(newPosition.y, moduleLength - roomLength)),
}
```

### 3. Key Constants

- **SCALE**: 4 pixels per foot (ensures grid alignment)
- **GRID_SIZE**: 4 feet (matches scale for perfect alignment)

### 4. Important Points

- `dragDelta` is tracked in state during drag
- Position is calculated in `handleDragEnd` using the stored delta
- Rooms snap to 4-foot grid increments
- Collision detection prevents overlapping
- Rooms are clamped to module boundaries

## Troubleshooting

### Rooms snap back
- **Cause**: `dragDelta` not being tracked or used correctly
- **Fix**: Ensure `handleDragOver` sets `dragDelta` and `handleDragEnd` uses it

### Rooms don't align to grid
- **Cause**: Grid spacing doesn't match scale
- **Fix**: Ensure GRID_SIZE = 4 and SCALE = 4 (they match)

### Transform not accessible
- **Cause**: useDraggable transform only available during render, not in events
- **Fix**: Use DragOverEvent delta instead of transform

