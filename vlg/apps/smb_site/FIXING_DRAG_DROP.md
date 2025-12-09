# 🔧 Fixing Drag/Drop - Implementation Notes

I see the issues. The drag/drop isn't working because:

1. **Position calculation is missing** - When dragging, we need to calculate WHERE the drop happened
2. **No collision detection** - Rooms are just placed at (0,0) without checking overlaps
3. **Drop zones not working** - Canvas and modules need proper droppable setup

## Fix Plan:

1. Use `DragOverEvent` to track position during drag
2. Calculate module-relative coordinates from mouse position
3. Use collision detection utilities to find valid position
4. Push other rooms when they collide
5. Add floor filtering UI
6. Add roof modules to library

**Working on comprehensive fix now...**

The main fix needed is in `handleDragEnd` - it needs to:
- Get the drop coordinates from the drag event
- Convert to module space  
- Find available position with collision detection
- Update room positions and push others

Let me implement this properly.

