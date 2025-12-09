"use client"

import React, { createContext, useContext, useState, ReactNode } from 'react'

interface DragPosition {
  x: number
  y: number
}

interface DragContextType {
  dragPosition: DragPosition | null
  setDragPosition: (position: DragPosition | null) => void
}

const DragContext = createContext<DragContextType | undefined>(undefined)

export function useDragPosition() {
  const context = useContext(DragContext)
  if (!context) {
    throw new Error('useDragPosition must be used within DragPositionProvider')
  }
  return context
}

export function DragPositionProvider({ children }: { children: ReactNode }) {
  const [dragPosition, setDragPosition] = useState<DragPosition | null>(null)
  return (
    <DragContext.Provider value={{ dragPosition, setDragPosition }}>
      {children}
    </DragContext.Provider>
  )
}

