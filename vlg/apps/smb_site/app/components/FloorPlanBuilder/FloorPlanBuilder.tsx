"use client"

import React, { useState } from 'react'
import { DndContext, DragEndEvent, DragStartEvent, DragOverEvent, DragOverlay, closestCenter } from '@dnd-kit/core'
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
import FloorPlanCanvas from './FloorPlanCanvas'
import RoomLibrary from './RoomLibrary'
import PricingDisplay from './PricingDisplay'
import FloorFilter, { type FloorFilter as FloorFilterType } from './FloorFilter'
import {
  findAvailablePosition,
  moveRoomWithCollision,
  snapToGrid,
} from '../../../lib/floorPlanUtils'
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
  const [dragDelta, setDragDelta] = useState<{ x: number; y: number } | null>(null)

  const handleDragStart = (event: DragStartEvent) => {
    setActiveId(event.active.id as string)
    setDragDelta(null) // Reset drag delta
  }

  const handleDragOver = (event: DragOverEvent) => {
    // Track drag delta during drag for position calculation
    if (event.delta) {
      setDragDelta({ x: event.delta.x, y: event.delta.y })
    }
  }

  const handleDragEnd = (event: DragEndEvent) => {
    const { active, over } = event
    
    if (!over) {
      setActiveId(null)
      return
    }

    // If dragging from library, add new room
    if (active.data.current?.source === 'library') {
      const roomType = active.data.current.roomType as RoomType
      const roomSize = STANDARD_ROOM_SIZES[roomType]
      
      // Find or create a module to place the room
      let targetModule: Module | null = null
      
      if (over.data.current?.type === 'module') {
        targetModule = over.data.current.module as Module
      } else if (over.id === 'canvas' || over.data.current?.type === 'canvas') {
        // Dropped on canvas - use first module or create new
        if (currentPlan.modules.length > 0) {
          targetModule = currentPlan.modules[0]
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
        // Use first module if no specific target
        targetModule = currentPlan.modules[0]
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

      if (targetModule) {
        const isMultiStory = roomType === 'vaulted-living' || roomType === 'staircase'
        
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
        const existingRooms = targetModule.rooms
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
        return
      }

      let targetModule: Module | null = null
      let newPosition: { x: number; y: number } = draggedRoom.position

      if (over.data.current?.type === 'module') {
        targetModule = over.data.current.module as Module
        newPosition = over.data.current.position || draggedRoom.position
      } else {
        targetModule = currentPlan.modules.find((m) => m.id === draggedRoom.moduleId) || null
      }

      if (targetModule) {
        // Use tracked drag delta to calculate new position
        if (dragDelta) {
          const SCALE = 4 // Match the canvas scale: 1 foot = 4 pixels
          const feetOffsetX = dragDelta.x / SCALE
          const feetOffsetY = dragDelta.y / SCALE
          newPosition = {
            x: draggedRoom.position.x + feetOffsetX,
            y: draggedRoom.position.y + feetOffsetY,
          }
        }

        // Snap to grid (align to 4-foot grid) and clamp to bounds
        newPosition = snapToGrid(newPosition, 4) // Use 4-foot grid
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
    setDragDelta(null) // Clear drag delta
  }

  const handleLoadTemplate = (plan: FloorPlan) => {
    // Deep copy the plan to preserve all room positions
    const copiedPlan: FloorPlan = {
      ...plan,
      modules: plan.modules.map((mod) => ({
        ...mod,
        rooms: mod.rooms.map((room) => ({ ...room })),
      })),
    }
    // Recalculate price and sqft
    copiedPlan.totalSqFt = calculateTotalSqFt(copiedPlan.modules)
    copiedPlan.estimatedPrice = calculateFloorPlanPrice(copiedPlan)
    setCurrentPlan(copiedPlan)
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

  return (
    <DndContext
      collisionDetection={closestCenter}
      onDragStart={handleDragStart}
      onDragOver={handleDragOver}
      onDragEnd={handleDragEnd}
    >
      <div className={styles.builderContainer}>
        <div className={styles.leftPanel}>
          <div className={styles.section}>
            <h3 className={styles.sectionTitle}>Floor Plans</h3>
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
          <div className={styles.topControls}>
            <FloorFilter value={floorFilter} onChange={setFloorFilter} />
          </div>
          <div className={styles.canvasContainer}>
            <FloorPlanCanvas
              floorPlan={floorFilter === 'all' ? currentPlan : {
                ...currentPlan,
                modules: currentPlan.modules.filter(m => m.level.toString() === floorFilter)
              }}
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

        <div className={styles.rightPanel}>
          <div className={styles.section}>
            <h3 className={styles.sectionTitle}>Room Library</h3>
            <RoomLibrary />
          </div>
        </div>
      </div>

      <DragOverlay>
        {activeId ? (
          <div className={styles.dragPreview}>
            {activeId.startsWith('room-') ? 'Room' : 'Module'}
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

