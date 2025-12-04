'use client'

import { useEffect, useState } from 'react'

interface DamagePopupProps {
  damage: number
  x: number
  y: number
  type?: 'damage' | 'heal' | 'miss'
  onComplete: () => void
}

export default function DamagePopup({ damage, x, y, type = 'damage', onComplete }: DamagePopupProps) {
  const [visible, setVisible] = useState(true)

  useEffect(() => {
    const timer = setTimeout(() => {
      setVisible(false)
      setTimeout(onComplete, 300)
    }, 1500)

    return () => clearTimeout(timer)
  }, [onComplete])

  if (!visible) return null

  const colors = {
    damage: '#ef4444',
    heal: '#4ade80',
    miss: '#888'
  }

  const symbols = {
    damage: '-',
    heal: '+',
    miss: 'MISS'
  }

  return (
    <div
      style={{
        position: 'fixed',
        left: `${x}px`,
        top: `${y}px`,
        color: colors[type],
        fontSize: '1.5rem',
        fontWeight: 'bold',
        pointerEvents: 'none',
        zIndex: 1000,
        textShadow: '2px 2px 4px rgba(0,0,0,0.8)',
        animation: 'floatUp 1.5s ease-out forwards',
        transform: 'translate(-50%, -50%)'
      }}
    >
      {type === 'miss' ? symbols[type] : `${symbols[type]}${damage}`}
      <style jsx>{`
        @keyframes floatUp {
          0% {
            opacity: 1;
            transform: translate(-50%, -50%) translateY(0);
          }
          100% {
            opacity: 0;
            transform: translate(-50%, -50%) translateY(-50px);
          }
        }
      `}</style>
    </div>
  )
}

