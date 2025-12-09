"use client"

import React from 'react'
import { useDraggable } from '@dnd-kit/core'
import { type RoomType, STANDARD_ROOM_SIZES } from '../../../lib/floorPlans'
import styles from './RoomLibrary.module.css'

const ROOM_TYPES: { type: RoomType; label: string; category: string; multiStory?: boolean }[] = [
  { type: 'kitchen', label: 'Kitchen', category: 'Living' },
  { type: 'living', label: 'Living Room', category: 'Living' },
  { type: 'vaulted-living', label: 'Vaulted Living (2-Story)', category: 'Living', multiStory: true },
  { type: 'dining', label: 'Dining Room', category: 'Living' },
  { type: 'bedroom-master', label: 'Master Bedroom', category: 'Bedrooms' },
  { type: 'bedroom-standard', label: 'Bedroom', category: 'Bedrooms' },
  { type: 'bathroom-full', label: 'Full Bath', category: 'Bathrooms' },
  { type: 'bathroom-half', label: 'Half Bath', category: 'Bathrooms' },
  { type: 'office', label: 'Office', category: 'Other' },
  { type: 'laundry', label: 'Laundry', category: 'Other' },
  { type: 'staircase', label: 'Staircase (2-Story)', category: 'Other', multiStory: true },
  { type: 'hallway', label: 'Hallway', category: 'Other' },
  { type: 'roof-gable', label: 'Gable Roof', category: 'Roof' },
  { type: 'roof-shed', label: 'Shed Roof', category: 'Roof' },
  { type: 'roof-hip', label: 'Hip Roof', category: 'Roof' },
]

export default function RoomLibrary() {
  const categories = Array.from(new Set(ROOM_TYPES.map((r) => r.category)))

  return (
    <div className={styles.library}>
      <h3 className={styles.libraryTitle}>Room Library</h3>
      <p className={styles.librarySubtitle}>
        Drag rooms onto the canvas to build your floor plan
      </p>

      {categories.map((category) => (
        <div key={category} className={styles.category}>
          <h4 className={styles.categoryTitle}>{category}</h4>
          <div className={styles.roomList}>
            {ROOM_TYPES.filter((r) => r.category === category).map((room) => (
              <DraggableRoom key={room.type} roomType={room.type} label={room.label} />
            ))}
          </div>
        </div>
      ))}
    </div>
  )
}

interface DraggableRoomProps {
  roomType: RoomType
  label: string
}

function DraggableRoom({ roomType, label }: DraggableRoomProps) {
  const { attributes, listeners, setNodeRef, transform, isDragging } = useDraggable({
    id: `library-${roomType}`,
    data: {
      source: 'library',
      roomType,
    },
  })

  const style = transform
    ? {
        transform: `translate3d(${transform.x}px, ${transform.y}px, 0)`,
      }
    : undefined

  const size = STANDARD_ROOM_SIZES[roomType]

  return (
    <div
      ref={setNodeRef}
      style={style}
      className={`${styles.roomItem} ${isDragging ? styles.roomItemDragging : ''}`}
      {...listeners}
      {...attributes}
    >
      <div className={styles.roomItemIcon}>
        <div className={styles.roomItemPreview} />
      </div>
      <div className={styles.roomItemInfo}>
        <div className={styles.roomItemName}>{label}</div>
        <div className={styles.roomItemSize}>
          {size.width}' × {size.length}'
        </div>
      </div>
    </div>
  )
}

