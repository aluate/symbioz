/**
 * Floor Plan Utility Functions
 * Collision detection, positioning, and room management
 */

import { type Room, type Module, type RoomType } from './floorPlans'

export interface Rect {
  x: number
  y: number
  width: number
  height: number
}

/**
 * Check if two rectangles overlap
 */
export function checkOverlap(rect1: Rect, rect2: Rect): boolean {
  return (
    rect1.x < rect2.x + rect2.width &&
    rect1.x + rect1.width > rect2.x &&
    rect1.y < rect2.y + rect2.height &&
    rect1.y + rect1.height > rect2.y
  )
}

/**
 * Get rectangle bounds for a room
 */
export function getRoomRect(room: Room): Rect {
  return {
    x: room.position.x,
    y: room.position.y,
    width: room.dimensions.width,
    height: room.dimensions.length,
  }
}

/**
 * Check if a room fits within a module
 */
export function roomFitsInModule(room: Room, module: Module): boolean {
  const roomRect = getRoomRect(room)
  return (
    roomRect.x >= 0 &&
    roomRect.y >= 0 &&
    roomRect.x + roomRect.width <= module.dimensions.width &&
    roomRect.y + roomRect.height <= module.dimensions.length
  )
}

/**
 * Check if a room collides with other rooms in a module
 */
export function checkRoomCollision(
  room: Room,
  otherRooms: Room[],
  excludeRoomId?: string
): Room | null {
  const roomRect = getRoomRect(room)
  
  for (const otherRoom of otherRooms) {
    if (excludeRoomId && otherRoom.id === excludeRoomId) continue
    
    const otherRect = getRoomRect(otherRoom)
    if (checkOverlap(roomRect, otherRect)) {
      return otherRoom
    }
  }
  
  return null
}

/**
 * Find a non-colliding position for a room in a module
 * Uses a grid-based approach to find available space
 */
export function findAvailablePosition(
  room: Room,
  module: Module,
  existingRooms: Room[],
  gridSize: number = 4, // Default to 4-foot grid
  preferredPosition?: { x: number; y: number }
): { x: number; y: number } | null {
  const moduleWidth = module.dimensions.width
  const moduleLength = module.dimensions.length
  const roomWidth = room.dimensions.width
  const roomLength = room.dimensions.length
  
  // If preferred position provided, try it first
  if (preferredPosition) {
    const testRoom: Room = {
      ...room,
      position: preferredPosition,
    }
    if (roomFitsInModule(testRoom, module) && !checkRoomCollision(testRoom, existingRooms)) {
      return preferredPosition
    }
  }
  
  // Try to find space after existing rooms, or spread out
  // Find the rightmost/bottommost existing room
  let maxRight = 0
  let maxBottom = 0
  for (const existingRoom of existingRooms) {
    const right = existingRoom.position.x + existingRoom.dimensions.width
    const bottom = existingRoom.position.y + existingRoom.dimensions.length
    maxRight = Math.max(maxRight, right)
    maxBottom = Math.max(maxBottom, bottom)
  }
  
  // Start searching from after existing rooms, or from the beginning
  const startX = maxRight + gridSize
  const startY = maxBottom + gridSize
  
  // Try positions starting from after existing rooms
  for (let y = startY; y <= moduleLength - roomLength; y += gridSize) {
    for (let x = startX; x <= moduleWidth - roomWidth; x += gridSize) {
      const testRoom: Room = {
        ...room,
        position: { x, y },
      }
      
      // Check if it fits and doesn't collide
      if (roomFitsInModule(testRoom, module)) {
        if (!checkRoomCollision(testRoom, existingRooms)) {
          return { x, y }
        }
      }
    }
  }
  
  // If no position found, try from the beginning
  for (let y = 0; y <= moduleLength - roomLength; y += gridSize) {
    for (let x = 0; x <= moduleWidth - roomWidth; x += gridSize) {
      const testRoom: Room = {
        ...room,
        position: { x, y },
      }
      
      if (roomFitsInModule(testRoom, module)) {
        if (!checkRoomCollision(testRoom, existingRooms)) {
          return { x, y }
        }
      }
    }
  }
  
  return null
}

/**
 * Snap position to grid (4-foot grid to match floor plan scale)
 */
export function snapToGrid(position: { x: number; y: number }, gridSize: number = 4): { x: number; y: number } {
  return {
    x: Math.round(position.x / gridSize) * gridSize,
    y: Math.round(position.y / gridSize) * gridSize,
  }
}

/**
 * Calculate drag position from mouse coordinates
 */
export function calculateDragPosition(
  event: { clientX: number; clientY: number },
  container: HTMLElement,
  scale: number = 0.8,
  gridSize: number = 2
): { x: number; y: number } {
  const rect = container.getBoundingClientRect()
  const x = (event.clientX - rect.left) / scale
  const y = (event.clientY - rect.top) / scale
  
  // Convert pixels to feet (assuming SCALE factor)
  const feetX = x / (scale * 0.8)
  const feetY = y / (scale * 0.8)
  
  // Snap to grid
  return snapToGrid({ x: feetX, y: feetY }, gridSize)
}

/**
 * Move room to new position, handling collisions by pushing other rooms
 */
export function moveRoomWithCollision(
  room: Room,
  newPosition: { x: number; y: number },
  module: Module,
  allRooms: Room[]
): { updatedRoom: Room; pushedRooms: Room[] } {
  const updatedRoom: Room = {
    ...room,
    position: newPosition,
  }
  
  // Check bounds
  if (!roomFitsInModule(updatedRoom, module)) {
    // Try to clamp to module bounds
    updatedRoom.position = {
      x: Math.max(0, Math.min(newPosition.x, module.dimensions.width - room.dimensions.width)),
      y: Math.max(0, Math.min(newPosition.y, module.dimensions.length - room.dimensions.length)),
    }
  }
  
  // Find collisions
  const collisions: Room[] = []
  const roomRect = getRoomRect(updatedRoom)
  
  for (const otherRoom of allRooms) {
    if (otherRoom.id === room.id) continue
    if (otherRoom.moduleId !== room.moduleId) continue
    
    const otherRect = getRoomRect(otherRoom)
    if (checkOverlap(roomRect, otherRect)) {
      collisions.push(otherRoom)
    }
  }
  
  // Push colliding rooms
  const pushedRooms: Room[] = []
  for (const collidingRoom of collisions) {
    const collisionRect = getRoomRect(collidingRoom)
    const pushX = roomRect.x + roomRect.width - collisionRect.x
    const pushY = roomRect.y + roomRect.height - collisionRect.y
    
    // Determine push direction (prefer horizontal push)
    const newPos = pushX > pushY 
      ? { x: collisionRect.x + pushX, y: collisionRect.y }
      : { x: collisionRect.x, y: collisionRect.y + pushY }
    
    // Clamp to module bounds
    const clampedPos = {
      x: Math.max(0, Math.min(newPos.x, module.dimensions.width - collidingRoom.dimensions.width)),
      y: Math.max(0, Math.min(newPos.y, module.dimensions.length - collidingRoom.dimensions.length)),
    }
    
    pushedRooms.push({
      ...collidingRoom,
      position: clampedPos,
    })
  }
  
  return { updatedRoom, pushedRooms }
}

