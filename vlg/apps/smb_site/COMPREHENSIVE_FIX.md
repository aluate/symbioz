# Comprehensive Floor Plan Builder Fix

## Issues to Fix:

1. **Rooms snapping back** - Drag position isn't being saved
2. **Grid alignment** - Modules and rooms don't align to grid
3. **Scale consistency** - Everything should use SCALE = 4 pixels/foot
4. **Visual layout** - Should look like floor plan, not bubbles

## Root Causes:

1. Transform from useDraggable isn't accessible in DragEndEvent
2. Grid spacing doesn't match scale ratio
3. Module positions aren't aligned to grid
4. Drag delta tracking not working properly

## Solutions:

1. Use DragOverEvent to track drag delta continuously
2. Store last drag position in state
3. Use that stored position in DragEndEvent
4. Ensure all positions snap to 4-foot grid
5. Align module positions to grid

**Implementing comprehensive fix now...**

