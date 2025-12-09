"use client"

import React, { useRef, useState } from 'react'
import { useDroppable, useDraggable, DragEndEvent, DragStartEvent } from '@dnd-kit/core'
import { type FloorPlan, type Module, type Room } from '../../../lib/floorPlans'
import styles from './FloorPlanCanvas.module.css'

interface FloorPlanCanvasProps {
  floorPlan: FloorPlan
  selectedRoom: Room | null
  onRoomSelect: (room: Room | null) => void
  onRoomDelete: (roomId: string) => void
}

export const SCALE = 4 // Scale factor: 1 foot = 4 pixels (for better visibility and grid alignment)
export const GRID_SIZE = 4 // Grid spacing in feet

export default function FloorPlanCanvas({
  floorPlan,
  selectedRoom,
  onRoomSelect,
  onRoomDelete,
}: FloorPlanCanvasProps) {
  const [showGrid, setShowGrid] = useState(true)
  const [zoom, setZoom] = useState(1)
  const canvasRef = useRef<HTMLDivElement>(null)

  // Calculate canvas size based on modules
  const maxWidth = Math.max(
    ...floorPlan.modules.map((m) => m.position.x + m.dimensions.width),
    16
  )
  const maxLength = Math.max(
    ...floorPlan.modules.map((m) => m.position.y + m.dimensions.length),
    65
  )

  const canvasWidth = maxWidth * SCALE
  const canvasHeight = maxLength * SCALE

  // Make canvas a droppable area
  const { setNodeRef: setCanvasRef, isOver: isCanvasOver } = useDroppable({
    id: 'canvas',
    data: {
      type: 'canvas',
    },
  })

  // Center the canvas content
  const canvasStyle: React.CSSProperties = {
    width: '100%',
    height: '100%',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    overflow: 'auto',
    position: 'relative',
  }

  const contentStyle: React.CSSProperties = {
    position: 'relative',
    width: `${canvasWidth * zoom}px`,
    height: `${canvasHeight * zoom}px`,
    minWidth: '800px',
    minHeight: '500px',
    transform: `scale(${zoom})`,
    transformOrigin: 'center center',
  }

  return (
    <div className={styles.canvasWrapper}>
      <div className={styles.canvasControls}>
        <button
          className={styles.controlButton}
          onClick={() => setShowGrid(!showGrid)}
        >
          {showGrid ? 'Hide' : 'Show'} Grid
        </button>
        <div className={styles.zoomControls}>
          <button
            className={styles.controlButton}
            onClick={() => setZoom(Math.max(0.5, zoom - 0.1))}
          >
            −
          </button>
          <span className={styles.zoomValue}>{Math.round(zoom * 100)}%</span>
          <button
            className={styles.controlButton}
            onClick={() => setZoom(Math.min(2, zoom + 0.1))}
          >
            +
          </button>
        </div>
      </div>

      <div
        ref={(node) => {
          setCanvasRef(node)
          canvasRef.current = node || undefined
        }}
        className={`${styles.canvas} ${isCanvasOver ? styles.canvasOver : ''}`}
        style={canvasStyle}
        onClick={(e) => {
          // Deselect room when clicking canvas
          if (e.target === e.currentTarget || (e.target as HTMLElement).classList.contains(styles.canvas)) {
            onRoomSelect(null)
          }
        }}
      >
        <div style={contentStyle}>
          {showGrid && (
            <svg 
              className={styles.grid} 
              width={canvasWidth} 
              height={canvasHeight}
              style={{
                position: 'absolute',
                top: 0,
                left: 0,
              }}
            >
              {Array.from({ length: Math.ceil(maxWidth / GRID_SIZE) + 1 }).map((_, i) => (
                <line
                  key={`v-${i}`}
                  x1={i * GRID_SIZE * SCALE}
                  y1={0}
                  x2={i * GRID_SIZE * SCALE}
                  y2={canvasHeight}
                  stroke="rgba(0,0,0,0.3)"
                  strokeWidth={1}
                />
              ))}
              {Array.from({ length: Math.ceil(maxLength / GRID_SIZE) + 1 }).map((_, i) => (
                <line
                  key={`h-${i}`}
                  x1={0}
                  y1={i * GRID_SIZE * SCALE}
                  x2={canvasWidth}
                  y2={i * GRID_SIZE * SCALE}
                  stroke="rgba(0,0,0,0.3)"
                  strokeWidth={1}
                />
              ))}
            </svg>
          )}

          {floorPlan.modules.map((module) => (
            <ModuleComponent
              key={module.id}
              module={module}
              selectedRoom={selectedRoom}
              onRoomSelect={onRoomSelect}
              onRoomDelete={onRoomDelete}
            />
          ))}

          {floorPlan.modules.length === 0 && (
            <div className={styles.emptyState}>
              <p className={styles.emptyText}>
                Start by loading a template or dragging rooms from the library
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

interface ModuleComponentProps {
  module: Module
  selectedRoom: Room | null
  onRoomSelect: (room: Room | null) => void
  onRoomDelete: (roomId: string) => void
}

function ModuleComponent({
  module,
  selectedRoom,
  onRoomSelect,
  onRoomDelete,
}: ModuleComponentProps) {
  const { setNodeRef, isOver } = useDroppable({
    id: `module-${module.id}`,
    data: {
      type: 'module',
      module,
    },
  })

  const moduleWidth = module.dimensions.width * SCALE
  const moduleLength = module.dimensions.length * SCALE

  return (
    <div
      ref={setNodeRef}
      className={`${styles.module} ${isOver ? styles.moduleOver : ''}`}
      style={{
        position: 'absolute',
        left: `${module.position.x * SCALE}px`,
        top: `${module.position.y * SCALE}px`,
        width: `${moduleWidth}px`,
        height: `${moduleLength}px`,
      }}
    >
      <div className={styles.moduleLabel}>
        Module {module.id.split('-').pop()} • Level {module.level}
      </div>
      {module.rooms.map((room) => (
        <RoomComponent
          key={room.id}
          room={room}
          module={module}
          isSelected={selectedRoom?.id === room.id}
          onSelect={() => onRoomSelect(room)}
          onDelete={() => onRoomDelete(room.id)}
        />
      ))}
    </div>
  )
}

interface RoomComponentProps {
  room: Room
  module: Module
  isSelected: boolean
  onSelect: () => void
  onDelete: () => void
}

function RoomComponent({
  room,
  module,
  isSelected,
  onSelect,
  onDelete,
}: RoomComponentProps) {
  const { attributes, listeners, setNodeRef, transform, isDragging } = useDraggable({
    id: room.id,
    data: {
      source: 'canvas',
      room,
      module,
      transform, // Pass transform so we can use it in drag end
    },
  })

  const style: React.CSSProperties = {
    position: 'absolute',
    left: `${room.position.x * SCALE}px`,
    top: `${room.position.y * SCALE}px`,
    ...(transform && {
      transform: `translate3d(${transform.x}px, ${transform.y}px, 0)`,
    }),
    cursor: isDragging ? 'grabbing' : 'grab',
    zIndex: isSelected ? 20 : isDragging ? 15 : 10,
  }

  const roomWidth = room.dimensions.width * SCALE
  const roomLength = room.dimensions.length * SCALE

  const roomColors: Record<string, string> = {
    kitchen: '#FFE5B4',
    'bedroom-master': '#E5F3FF',
    'bedroom-standard': '#E5F3FF',
    'bathroom-full': '#E5FFE5',
    'bathroom-half': '#E5FFE5',
    living: '#FFE5E5',
    'vaulted-living': '#FFCCCC',
    dining: '#FFF5E5',
    office: '#F5E5FF',
    laundry: '#E5E5E5',
    staircase: '#D5D5D5',
    hallway: '#F5F5F5',
    'roof-gable': '#E8E8E8',
    'roof-shed': '#E0E0E0',
    'roof-hip': '#D8D8D8',
  }

  return (
    <div
      ref={setNodeRef}
      style={style}
      className={`${styles.room} ${isSelected ? styles.roomSelected : ''} ${isDragging ? styles.roomDragging : ''}`}
      onClick={(e) => {
        e.stopPropagation()
        onSelect()
      }}
      {...listeners}
      {...attributes}
    >
      <div
        className={styles.roomFill}
        style={{
          backgroundColor: roomColors[room.type] || '#F0F0F0',
          width: `${roomWidth}px`,
          height: `${roomLength}px`,
        }}
      >
        <div className={styles.roomLabel}>{room.name}</div>
        <div className={styles.roomSize}>
          {room.dimensions.width}' × {room.dimensions.length}'
        </div>
      </div>
    </div>
  )
}
