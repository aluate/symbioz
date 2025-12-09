# Drag and Drop Fix - Implementation Plan

## Current Problems
1. Drag and drop not working - rooms won't drag from library
2. No collision detection - rooms can stack
3. Position calculation not working
4. Need floor filtering
5. Need roof modules and multi-story rooms

## Fix Strategy

### Phase 1: Fix Basic Drag/Drop
- Use `@dnd-kit` sensors for better drag handling
- Calculate drop position from drag coordinates
- Properly handle canvas and module drop zones

### Phase 2: Add Collision Detection  
- Use floorPlanUtils.ts collision functions
- Push rooms when they collide
- Validate bounds

### Phase 3: Add Features
- Floor filter UI
- Roof modules
- Multi-story rooms

## Implementation Notes

The drag/drop needs to:
1. Get mouse coordinates during drag
2. Convert to module-relative coordinates
3. Check collisions with existing rooms
4. Push colliding rooms
5. Update room positions

Let me implement the complete fix now...

