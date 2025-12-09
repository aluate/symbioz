"use client"

import React, { useState } from 'react'
import { DndContext, DragEndEvent, DragStartEvent, DragOverlay, DragOverEvent } from '@dnd-kit/core'
import { 
  type FloorPlan, 
  type Module, 
  type Room, 
  type RoomType,
  DEFAULT_FLOOR_PLANS,
  calculateFloorPlanPrice,
  calculateTotalSqFt,
  STANDARD_ROOM_SIZES
} from '../../../lib/floorPlans'
import {
  findAvailablePosition,
  moveRoomWithCollision,
  snapToGrid,
  checkRoomCollision,
  roomFitsInModule,
} from '../../../lib/floorPlanUtils'
import FloorPlanCanvas from './FloorPlanCanvas'
import RoomLibrary from './RoomLibrary'
import PricingDisplay from './PricingDisplay'
import FloorFilter, { type FloorFilter as FloorFilterType } from './FloorFilter'
import styles from './FloorPlanBuilder.module.css'

interface FloorPlanBuilderProps {
  initialPlan?: FloorPlan
}

export default function FloorPlanBuilder({ initialPlan }: FloorPlanBuilderProps) {
  const [currentPlan, setCurrentPlan] = useState<FloorPlan>(
    initialPlan || {
      id: 'custom',
      name: 'Custom Plan',
      description: '',
      modules: [],
      estimatedPrice: 0,
      totalSqFt: 0,
    }
  )
  const [activeId, setActiveId] = useState<string | null>(null)
  const [selectedRoom, setSelectedRoom] = useState<Room | null>(null)
  const [floorFilter, setFloorFilter] = useState<FloorFilterType>('all')
  const [dragPosition, setDragPosition] = useState<{ x: number; y: number } | null>(null)

  // Filter modules by floor level
  const filteredModules = currentPlan.modules.filter((module) => {
    if (floorFilter === 'all') return true
    return module.level.toString() === floorFilter
  })

  const handleDragStart = (event: DragStartEvent) => {
    setActiveId(event.active.id as string)
  }

  const handleDragOver = (event: DragOverEvent) => {
    // Track drag position for position calculation
    if (event.over?.rect) {
      // We'll calculate position in dragEnd from the drop location
    }
  }

  const handleDragEnd = (event: DragEndEvent) => {
    const { active, over } = event
    
    if (!over) {
      setActiveId(null)
      setDragPosition(null)
      return
    }

    // If dragging from library, add new room
    if (active.data.current?.source === 'library') {
      const roomType = active.data.current.roomType as RoomType
      const roomSize = STANDARD_ROOM_SIZES[roomType]
      
      // Determine target module
      let targetModule: Module | null = null
      
      if (over.data.current?.type === 'module') {
        targetModule = over.data.current.module as Module
      } else if (over.id === 'canvas' || over.data.current?.type === 'canvas') {
        // Dropped on canvas - use first module or create new
        if (currentPlan.modules.length > 0) {
          // Filter by current floor filter if active
          const availableModules = floorFilter === 'all' 
            ? currentPlan.modules 
            : currentPlan.modules.filter(m => m.level.toString() === floorFilter)
          targetModule = availableModules[0] || currentPlan.modules[0]
        } else {
          // Create new module if none exist
          targetModule = {
            id: `mod-${Date.now()}`,
            dimensions: { width: 16, length: 65 },
            position: { x: 0, y: 0 },
            level: 1,
            rooms: [],
          }
        }
      } else if (currentPlan.modules.length > 0) {
        targetModule = currentPlan.modules[0]
      } else {
        targetModule = {
          id: `mod-${Date.now()}`,
          dimensions: { width: 16, length: 65 },
          position: { x: 0, y: 0 },
          level: 1,
          rooms: [],
        }
      }

      if (targetModule) {
        // Check if room type supports multi-story
        const isMultiStory = roomType === 'vaulted-living' || roomType === 'staircase'
        const isRoof = roomType.startsWith('roof-')
        
        const newRoom: Room = {
          id: `room-${Date.now()}`,
          type: roomType,
          name: getRoomName(roomType),
          dimensions: roomSize,
          position: { x: 0, y: 0 },
          moduleId: targetModule.id,
          isMultiStory: isMultiStory,
          levels: isMultiStory ? [1, 2] : undefined,
        }

        // Find available position using collision detection
        const existingRooms = targetModule.rooms.filter(r => r.id !== newRoom.id)
        const availablePos = findAvailablePosition(newRoom, targetModule, existingRooms)
        
        if (availablePos) {
          newRoom.position = availablePos
        }

        const updatedModules = currentPlan.modules.map((mod) =>
          mod.id === targetModule!.id
            ? { ...mod, rooms: [...mod.rooms, newRoom] }
            : mod
        )

        // If module was new, add it
        if (!currentPlan.modules.find((m) => m.id === targetModule!.id)) {
          updatedModules.push(targetModule)
        }

        const updatedPlan: FloorPlan = {
          ...currentPlan,
          modules: updatedModules,
          totalSqFt: calculateTotalSqFt(updatedModules),
        }
        updatedPlan.estimatedPrice = calculateFloorPlanPrice(updatedPlan)

        setCurrentPlan(updatedPlan)
      }
    }

    // If dragging existing room, update position with collision detection
    if (active.data.current?.source === 'canvas') {
      const roomId = active.id as string
      const draggedRoom = currentPlan.modules
        .flatMap((m) => m.rooms)
        .find((r) => r.id === roomId)
      
      if (!draggedRoom) {
        setActiveId(null)
        setDragPosition(null)
        return
      }

      let targetModule: Module | null = null
      let newPosition: { x: number; y: number } = draggedRoom.position

      if (over.data.current?.type === 'module') {
        targetModule = over.data.current.module as Module
        // Use position from drag if available, otherwise keep current
        newPosition = over.data.current.position || draggedRoom.position
      } else {
        // Find the room's current module
        targetModule = currentPlan.modules.find((m) => m.id === draggedRoom.moduleId) || null
      }

      if (targetModule) {
        // Snap to grid
        newPosition = snapToGrid(newPosition, 2)

        // Clamp to module bounds
        newPosition = {
          x: Math.max(0, Math.min(newPosition.x, targetModule.dimensions.width - draggedRoom.dimensions.width)),
          y: Math.max(0, Math.min(newPosition.y, targetModule.dimensions.length - draggedRoom.dimensions.length)),
        }

        const testRoom: Room = {
          ...draggedRoom,
          position: newPosition,
          moduleId: targetModule.id,
        }

        // Use collision detection to move room and push others
        const otherRooms = targetModule.rooms.filter((r) => r.id !== roomId)
        const { updatedRoom, pushedRooms } = moveRoomWithCollision(
          testRoom,
          newPosition,
          targetModule,
          otherRooms
        )

        // Update all rooms in the module
        const allUpdatedRooms = [
          updatedRoom,
          ...pushedRooms,
          ...otherRooms.filter((r) => !pushedRooms.some((pr) => pr.id === r.id)),
        ]

        const updatedModules = currentPlan.modules.map((mod) => {
          if (mod.id === targetModule!.id) {
            return {
              ...mod,
              rooms: allUpdatedRooms,
            }
          } else {
            // Remove room from other modules
            return {
              ...mod,
              rooms: mod.rooms.filter((r) => r.id !== roomId),
            }
          }
        })

        const updatedPlan: FloorPlan = {
          ...currentPlan,
          modules: updatedModules,
          totalSqFt: calculateTotalSqFt(updatedModules),
        }
        updatedPlan.estimatedPrice = calculateFloorPlanPrice(updatedPlan)

        setCurrentPlan(updatedPlan)
      }
    }

    setActiveId(null)
    setDragPosition(null)
  }

  const handleLoadTemplate = (plan: FloorPlan) => {
    setCurrentPlan(plan)
    setSelectedRoom(null)
  }

  const handleDeleteRoom = (roomId: string) => {
    const updatedModules = currentPlan.modules.map((mod) => ({
      ...mod,
      rooms: mod.rooms.filter((r) => r.id !== roomId),
    }))

    const updatedPlan: FloorPlan = {
      ...currentPlan,
      modules: updatedModules,
      totalSqFt: calculateTotalSqFt(updatedModules),
    }
    updatedPlan.estimatedPrice = calculateFloorPlanPrice(updatedPlan)

    setCurrentPlan(updatedPlan)
    setSelectedRoom(null)
  }

  const handleRoomSelect = (room: Room | null) => {
    setSelectedRoom(room)
  }

  // Filter floor plan for display
  const filteredPlan: FloorPlan = {
    ...currentPlan,
    modules: filteredModules,
  }

  return (
    <DndContext
      onDragStart={handleDragStart}
      onDragOver={handleDragOver}
      onDragEnd={handleDragEnd}
    >
      <div className={styles.builderContainer}>
        <div className={styles.sidebar}>
          <FloorFilter value={floorFilter} onChange={setFloorFilter} />
          <RoomLibrary />
          <div className={styles.templatesSection}>
            <h3 className={styles.sidebarTitle}>Start with a Template</h3>
            <div className={styles.templateList}>
              {DEFAULT_FLOOR_PLANS.map((plan) => (
                <button
                  key={plan.id}
                  className={styles.templateButton}
                  onClick={() => handleLoadTemplate(plan)}
                >
                  <div className={styles.templateName}>{plan.name}</div>
                  <div className={styles.templateDetails}>
                    {plan.modules.length} module{plan.modules.length !== 1 ? 's' : ''} • {plan.totalSqFt.toLocaleString()} sq ft
                  </div>
                </button>
              ))}
            </div>
          </div>
        </div>

        <div className={styles.mainArea}>
          <div className={styles.canvasContainer}>
            <FloorPlanCanvas
              floorPlan={filteredPlan}
              selectedRoom={selectedRoom}
              onRoomSelect={handleRoomSelect}
              onRoomDelete={handleDeleteRoom}
            />
          </div>

          <div className={styles.infoPanel}>
            <PricingDisplay floorPlan={currentPlan} />
            {selectedRoom && (
              <div className={styles.roomInfo}>
                <h4 className={styles.roomInfoTitle}>{selectedRoom.name}</h4>
                <div className={styles.roomInfoDetails}>
                  <div>
                    <span className={styles.roomInfoLabel}>Type:</span> {selectedRoom.type}
                  </div>
                  <div>
                    <span className={styles.roomInfoLabel}>Size:</span>{' '}
                    {selectedRoom.dimensions.width}' × {selectedRoom.dimensions.length}'
                  </div>
                  <div>
                    <span className={styles.roomInfoLabel}>Area:</span>{' '}
                    {selectedRoom.dimensions.width * selectedRoom.dimensions.length} sq ft
                  </div>
                  {selectedRoom.isMultiStory && (
                    <div>
                      <span className={styles.roomInfoLabel}>Multi-Story:</span> Yes (spans 2 floors)
                    </div>
                  )}
                </div>
                <button
                  className={styles.deleteButton}
                  onClick={() => handleDeleteRoom(selectedRoom.id)}
                >
                  Remove Room
                </button>
              </div>
            )}
          </div>
        </div>
      </div>

      <DragOverlay>
        {activeId ? (
          <div className={styles.dragPreview}>
            {activeId.startsWith('room-') || activeId.startsWith('library-') ? 'Room' : 'Module'}
          </div>
        ) : null}
      </DragOverlay>
    </DndContext>
  )
}

function getRoomName(type: RoomType): string {
  const names: Record<RoomType, string> = {
    kitchen: 'Kitchen',
    'bedroom-master': 'Master Bedroom',
    'bedroom-standard': 'Bedroom',
    'bathroom-full': 'Full Bath',
    'bathroom-half': 'Half Bath',
    living: 'Living Room',
    dining: 'Dining Room',
    office: 'Office',
    laundry: 'Laundry',
    staircase: 'Staircase',
    hallway: 'Hallway',
    'vaulted-living': 'Vaulted Living Room',
    'roof-gable': 'Gable Roof',
    'roof-shed': 'Shed Roof',
    'roof-hip': 'Hip Roof',
  }
  return names[type] || type
}

