/**
 * Floor Plan Data Structures and Default Templates
 * For Sugar Mountain Builders modular home system
 */

export type RoomType =
  | 'kitchen'
  | 'bedroom-master'
  | 'bedroom-standard'
  | 'bathroom-full'
  | 'bathroom-half'
  | 'living'
  | 'dining'
  | 'office'
  | 'laundry'
  | 'staircase'
  | 'hallway'
  | 'vaulted-living'
  | 'roof-gable'
  | 'roof-shed'
  | 'roof-hip'

export interface Room {
  id: string
  type: RoomType
  name: string
  dimensions: {
    width: number // feet
    length: number // feet
  }
  position: {
    x: number // feet from module origin
    y: number // feet from module origin
  }
  moduleId: string
  levels?: (1 | 2)[] // Which floor levels this room spans (default: [module.level])
  isMultiStory?: boolean // True for vaulted ceilings, staircases, etc.
}

export type ModuleType = 'standard' | 'roof'

export interface Module {
  id: string
  type?: ModuleType // 'standard' or 'roof' (default: 'standard')
  dimensions: {
    width: number // feet (typically 16)
    length: number // feet (typically 65 or 70)
  }
  position: {
    x: number // feet from plan origin
    y: number // feet from plan origin
  }
  level: 1 | 2 // floor level (roof modules are level 3 conceptually, but stored as 2)
  rooms: Room[]
}

export interface FloorPlan {
  id: string
  name: string
  description: string
  modules: Module[]
  estimatedPrice: number // base price in dollars
  totalSqFt: number
}

// Standard room sizes (in square feet)
export const STANDARD_ROOM_SIZES: Record<RoomType, { width: number; length: number }> = {
  kitchen: { width: 15, length: 16 },
  'bedroom-master': { width: 15, length: 16 },
  'bedroom-standard': { width: 12, length: 14 },
  'bathroom-full': { width: 8, length: 10 },
  'bathroom-half': { width: 6, length: 8 },
  living: { width: 16, length: 20 }, // Variable, this is default
  dining: { width: 12, length: 14 },
  office: { width: 12, length: 12 },
  laundry: { width: 8, length: 8 },
  staircase: { width: 4, length: 8 },
  hallway: { width: 4, length: 10 },
  'vaulted-living': { width: 16, length: 25 }, // Can span 2 floors
  'roof-gable': { width: 16, length: 65 }, // Full module roof
  'roof-shed': { width: 16, length: 65 },
  'roof-hip': { width: 16, length: 65 },
}

// Base pricing per module (simplified)
const BASE_MODULE_PRICE = 80000 // $80k per module base
const PRICE_PER_SQFT = 150 // $150/sqft for finishes

export function calculateFloorPlanPrice(floorPlan: FloorPlan): number {
  const modulePrice = floorPlan.modules.length * BASE_MODULE_PRICE
  const finishPrice = floorPlan.totalSqFt * PRICE_PER_SQFT
  return modulePrice + finishPrice
}

export function calculateTotalSqFt(modules: Module[]): number {
  return modules.reduce((total, module) => {
    return total + module.dimensions.width * module.dimensions.length
  }, 0)
}

// Default Floor Plan: Sugarline 65 (Single Module, 16x65)
export const SUGARLINE_65: FloorPlan = {
  id: 'sugarline-65',
  name: 'Sugarline 65',
  description: 'A single-module foundation perfect for starter homes, guest houses, or ADUs.',
  modules: [
    {
      id: 'mod-1',
      dimensions: { width: 16, length: 65 },
      position: { x: 0, y: 0 },
      level: 1,
      rooms: [
        {
          id: 'room-kitchen-1',
          type: 'kitchen',
          name: 'Kitchen',
          dimensions: { width: 15, length: 16 },
          position: { x: 0, y: 0 },
          moduleId: 'mod-1',
        },
        {
          id: 'room-living-1',
          type: 'living',
          name: 'Living Room',
          dimensions: { width: 16, length: 25 },
          position: { x: 0, y: 16 },
          moduleId: 'mod-1',
        },
        {
          id: 'room-bedroom-1',
          type: 'bedroom-master',
          name: 'Master Bedroom',
          dimensions: { width: 15, length: 16 },
          position: { x: 0, y: 41 },
          moduleId: 'mod-1',
        },
        {
          id: 'room-bathroom-1',
          type: 'bathroom-full',
          name: 'Bathroom',
          dimensions: { width: 8, length: 10 },
          position: { x: 8, y: 41 },
          moduleId: 'mod-1',
        },
      ],
    },
  ],
  estimatedPrice: 200000,
  totalSqFt: 1040,
}

// Default Floor Plan: Twinline 130 (Two Modules Offset, 2x16x65)
export const TWINLINE_130: FloorPlan = {
  id: 'twinline-130',
  name: 'Twinline 130',
  description: 'Two modules in an offset configuration, perfect for families seeking split-floor-plan living.',
  modules: [
    {
      id: 'mod-1',
      dimensions: { width: 16, length: 65 },
      position: { x: 0, y: 0 },
      level: 1,
      rooms: [
        {
          id: 'room-bedroom-1',
          type: 'bedroom-master',
          name: 'Master Suite',
          dimensions: { width: 15, length: 16 },
          position: { x: 0, y: 0 },
          moduleId: 'mod-1',
        },
        {
          id: 'room-bathroom-1',
          type: 'bathroom-full',
          name: 'Master Bath',
          dimensions: { width: 8, length: 10 },
          position: { x: 8, y: 0 },
          moduleId: 'mod-1',
        },
        {
          id: 'room-kitchen-1',
          type: 'kitchen',
          name: 'Kitchen',
          dimensions: { width: 15, length: 16 },
          position: { x: 0, y: 16 },
          moduleId: 'mod-1',
        },
        {
          id: 'room-living-1',
          type: 'living',
          name: 'Great Room',
          dimensions: { width: 16, length: 33 },
          position: { x: 0, y: 32 },
          moduleId: 'mod-1',
        },
      ],
    },
    {
      id: 'mod-2',
      dimensions: { width: 16, length: 65 },
      position: { x: 18, y: 0 }, // Offset by 2 feet
      level: 1,
      rooms: [
        {
          id: 'room-bedroom-2',
          type: 'bedroom-standard',
          name: 'Bedroom 2',
          dimensions: { width: 12, length: 14 },
          position: { x: 0, y: 0 },
          moduleId: 'mod-2',
        },
        {
          id: 'room-bedroom-3',
          type: 'bedroom-standard',
          name: 'Bedroom 3',
          dimensions: { width: 12, length: 14 },
          position: { x: 0, y: 16 },
          moduleId: 'mod-2',
        },
        {
          id: 'room-bathroom-2',
          type: 'bathroom-full',
          name: 'Guest Bath',
          dimensions: { width: 8, length: 10 },
          position: { x: 12, y: 0 },
          moduleId: 'mod-2',
        },
        {
          id: 'room-office-1',
          type: 'office',
          name: 'Office',
          dimensions: { width: 12, length: 12 },
          position: { x: 0, y: 32 },
          moduleId: 'mod-2',
        },
      ],
    },
  ],
  estimatedPrice: 400000,
  totalSqFt: 2080,
}

// Default Floor Plan: Summit Stack (Four Modules, Two-Story)
export const SUMMIT_STACK: FloorPlan = {
  id: 'summit-stack',
  name: 'Summit Stack',
  description: 'Four modules in a two-story configuration, creating a spacious mountain estate home.',
  modules: [
    // First floor modules
    {
      id: 'mod-1-f1',
      dimensions: { width: 16, length: 65 },
      position: { x: 0, y: 0 },
      level: 1,
      rooms: [
        {
          id: 'room-kitchen-1',
          type: 'kitchen',
          name: 'Kitchen',
          dimensions: { width: 15, length: 16 },
          position: { x: 0, y: 0 },
          moduleId: 'mod-1-f1',
        },
        {
          id: 'room-dining-1',
          type: 'dining',
          name: 'Dining Room',
          dimensions: { width: 12, length: 14 },
          position: { x: 0, y: 16 },
          moduleId: 'mod-1-f1',
        },
        {
          id: 'room-living-1',
          type: 'living',
          name: 'Great Room',
          dimensions: { width: 16, length: 35 },
          position: { x: 0, y: 30 },
          moduleId: 'mod-1-f1',
        },
      ],
    },
    {
      id: 'mod-2-f1',
      dimensions: { width: 16, length: 65 },
      position: { x: 18, y: 0 },
      level: 1,
      rooms: [
        {
          id: 'room-office-1',
          type: 'office',
          name: 'Office',
          dimensions: { width: 12, length: 12 },
          position: { x: 0, y: 0 },
          moduleId: 'mod-2-f1',
        },
        {
          id: 'room-laundry-1',
          type: 'laundry',
          name: 'Laundry',
          dimensions: { width: 8, length: 8 },
          position: { x: 12, y: 0 },
          moduleId: 'mod-2-f1',
        },
        {
          id: 'room-staircase-1',
          type: 'staircase',
          name: 'Staircase',
          dimensions: { width: 4, length: 8 },
          position: { x: 0, y: 16 },
          moduleId: 'mod-2-f1',
        },
        {
          id: 'room-bathroom-1',
          type: 'bathroom-half',
          name: 'Powder Room',
          dimensions: { width: 6, length: 8 },
          position: { x: 6, y: 16 },
          moduleId: 'mod-2-f1',
        },
      ],
    },
    // Second floor modules
    {
      id: 'mod-1-f2',
      dimensions: { width: 16, length: 65 },
      position: { x: 0, y: 0 },
      level: 2,
      rooms: [
        {
          id: 'room-bedroom-1',
          type: 'bedroom-master',
          name: 'Master Suite',
          dimensions: { width: 15, length: 16 },
          position: { x: 0, y: 0 },
          moduleId: 'mod-1-f2',
        },
        {
          id: 'room-bathroom-2',
          type: 'bathroom-full',
          name: 'Master Bath',
          dimensions: { width: 8, length: 10 },
          position: { x: 8, y: 0 },
          moduleId: 'mod-1-f2',
        },
        {
          id: 'room-office-2',
          type: 'office',
          name: 'Sitting Room',
          dimensions: { width: 12, length: 12 },
          position: { x: 0, y: 16 },
          moduleId: 'mod-1-f2',
        },
      ],
    },
    {
      id: 'mod-2-f2',
      dimensions: { width: 16, length: 65 },
      position: { x: 18, y: 0 },
      level: 2,
      rooms: [
        {
          id: 'room-bedroom-2',
          type: 'bedroom-standard',
          name: 'Bedroom 2',
          dimensions: { width: 12, length: 14 },
          position: { x: 0, y: 0 },
          moduleId: 'mod-2-f2',
        },
        {
          id: 'room-bedroom-3',
          type: 'bedroom-standard',
          name: 'Bedroom 3',
          dimensions: { width: 12, length: 14 },
          position: { x: 0, y: 16 },
          moduleId: 'mod-2-f2',
        },
        {
          id: 'room-bathroom-3',
          type: 'bathroom-full',
          name: 'Guest Bath',
          dimensions: { width: 8, length: 10 },
          position: { x: 12, y: 0 },
          moduleId: 'mod-2-f2',
        },
      ],
    },
  ],
  estimatedPrice: 800000,
  totalSqFt: 4160,
}

export const DEFAULT_FLOOR_PLANS: FloorPlan[] = [
  SUGARLINE_65,
  TWINLINE_130,
  SUMMIT_STACK,
]

export function getFloorPlanById(id: string): FloorPlan | undefined {
  return DEFAULT_FLOOR_PLANS.find((plan) => plan.id === id)
}

