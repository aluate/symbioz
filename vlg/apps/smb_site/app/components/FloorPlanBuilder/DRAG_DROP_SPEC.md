# Drag and Drop Implementation Specification

## Overview
The floor plan builder uses `@dnd-kit/core` for drag and drop functionality. Rooms can be dragged from the library onto modules, and existing rooms can be dragged to new positions within modules.

## Current Implementation

### Scale & Grid
- **SCALE**: 4 pixels per foot (ensures grid alignment)
- **GRID_SIZE**: 4 feet (matches scale for perfect alignment)

### Drag Tracking
1. **DragStart**: Sets active ID, resets drag delta
2. **DragOver**: Tracks drag delta continuously (event.delta.x, event.delta.y)
3. **DragEnd**: Uses tracked delta to calculate final position

### Position Calculation
```typescript
// Convert pixel delta to feet
const SCALE = 4 // 1 foot = 4 pixels
const feetOffsetX = dragDelta.x / SCALE
const feetOffsetY = dragDelta.y / SCALE

// Add to original position
newPosition = {
  x: draggedRoom.position.x + feetOffsetX,
  y: draggedRoom.position.y + feetOffsetY,
}

// Snap to grid (4-foot increments)
newPosition = snapToGrid(newPosition, 4)
```

### Collision Detection
- Uses `moveRoomWithCollision()` to push other rooms when dragging
- Rooms cannot overlap
- Rooms are clamped to module boundaries

## Known Issues

1. **Rooms snap back**: If dragDelta isn't tracked properly, position isn't updated
2. **Transform not accessible**: useDraggable transform isn't available in DragEndEvent
3. **Grid alignment**: Need to ensure all positions snap to 4-foot grid

## Solution

Use DragOverEvent to continuously track delta:
```typescript
const handleDragOver = (event: DragOverEvent) => {
  if (event.delta) {
    setDragDelta({ x: event.delta.x, y: event.delta.y })
  }
}
```

Then use dragDelta in DragEndEvent to calculate final position.

## Testing Checklist

- [ ] Rooms stay where dropped (no snap back)
- [ ] Rooms align to grid
- [ ] Collision detection works (rooms push each other)
- [ ] Rooms can't be dragged outside module bounds
- [ ] New rooms from library can be placed correctly

