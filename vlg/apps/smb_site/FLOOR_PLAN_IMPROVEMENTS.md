# Floor Plan Builder - Planned Improvements

**Status:** In Progress

## ✅ Completed
- Basic drag and drop structure
- Template loading
- Pricing display

## 🔧 In Progress

### 1. Fix Drag and Drop (CRITICAL)
- [ ] Rooms from library should drop onto canvas/modules
- [ ] Rooms should move other rooms when dragged (collision detection)
- [ ] Rooms can't stack on top of each other
- [ ] Proper position calculation from drag coordinates

### 2. Add Collision Detection
- [ ] Check room overlaps
- [ ] Push other rooms when dragging
- [ ] Snap to grid for alignment
- [ ] Validate room fits within module bounds

### 3. Floor Level Filtering
- [ ] Filter UI to show Level 1, Level 2, or Both
- [ ] Filter modules by level
- [ ] Filter rooms by their level property

### 4. Multi-Story Room Support
- [ ] Mark rooms as multi-story (vaulted-living, staircase)
- [ ] Display on both levels
- [ ] Special handling for spanning rooms

### 5. Roof Modules
- [ ] Add roof module types (gable, shed, hip)
- [ ] Add to room library
- [ ] Display on top of modules
- [ ] Pricing adjustment for roof modules

## 🎯 Next Steps

1. **Fix drag/drop handler** - Use proper coordinate calculation
2. **Add collision utilities** - Use floorPlanUtils.ts functions
3. **Update RoomLibrary** - Add roof modules and vaulted-living
4. **Add floor filter UI** - Toggle between levels
5. **Test everything** - Make sure rooms move each other properly

---

**Working on these improvements now!**

