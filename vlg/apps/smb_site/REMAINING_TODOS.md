# Remaining TODOs for Floor Plan Builder

Based on the current todo list, here are the remaining items:

## Current Status

### ✅ Completed
1. ✅ Fix drag and drop - rooms should move properly and not stack
2. ✅ Fix room positioning - rooms appearing in top right corner, need proper spacing
3. ✅ Improve visual layout - make modules look like floor plan containers, not bubbles
4. ✅ Fix layout - separate floor toggle, room list, and floor plans

### ⏳ In Progress
5. 🔧 Fix runtime errors and test drag and drop functionality

### 📋 Pending/Remaining

6. **Add floor level filtering UI** (Already partially done - FloorFilter component exists)
   - ✅ Component created
   - Need to verify it works correctly with filtering

7. **Add multi-story room support** (vaulted ceilings, staircases)
   - ✅ Data structures support it (isMultiStory, levels properties)
   - ✅ Vaulted-living and staircase room types added
   - Need to verify visual representation works correctly

8. **Add roof module types and support**
   - ✅ Data structures support it (RoofModule interface)
   - ✅ Roof types added to RoomLibrary (roof-gable, roof-shed, roof-hip)
   - Need to verify they render and work correctly

9. **Improve drag position calculation to snap to grid**
   - ✅ Grid snapping implemented (4-foot grid)
   - Need to verify rooms actually snap correctly when dropped

10. **Additional enhancements needed:**
    - Verify collision detection works when moving rooms
    - Test that rooms stay where dropped (no snap back)
    - Ensure grid lines are visible and align properly
    - Test all drag and drop scenarios

## Summary

The **5 remaining todos** that need attention:
1. Fix runtime errors and test drag/drop (in progress)
2. Verify floor filtering works correctly
3. Verify multi-story rooms display correctly
4. Verify roof modules render and work
5. Test and refine grid snapping behavior

All the major features are built, but they need testing and refinement to ensure they work correctly!

