'use client'

import { useEffect, useState } from 'react'

/**
 * Optional Otto diagnostics component
 * Only renders if NEXT_PUBLIC_OTTO_BASE_URL is set
 */
export default function OttoDiagnostics() {
  const [status, setStatus] = useState<'checking' | 'healthy' | 'unhealthy' | 'not-configured' | null>(null)
  const ottoUrl = process.env.NEXT_PUBLIC_OTTO_BASE_URL

  useEffect(() => {
    if (!ottoUrl) {
      setStatus('not-configured')
      return
    }

    setStatus('checking')
    fetch(`${ottoUrl}/health`)
      .then(res => res.json())
      .then(() => {
        setStatus('healthy')
        console.log('[Otto] Health check passed')
      })
      .catch(() => {
        setStatus('unhealthy')
        console.warn('[Otto] Health check failed')
      })
  }, [ottoUrl])

  // Only show in development or if explicitly configured
  if (!ottoUrl || process.env.NODE_ENV === 'production') {
    return null
  }

  return (
    <div style={{
      position: 'fixed',
      bottom: '10px',
      right: '10px',
      padding: '8px 12px',
      backgroundColor: status === 'healthy' ? '#10b981' : status === 'unhealthy' ? '#ef4444' : '#6b7280',
      color: 'white',
      borderRadius: '4px',
      fontSize: '12px',
      zIndex: 9999,
      opacity: 0.8
    }}>
      {status === 'checking' && 'Otto: Checking...'}
      {status === 'healthy' && 'Otto: ✓ Healthy'}
      {status === 'unhealthy' && 'Otto: ✗ Unhealthy'}
      {status === 'not-configured' && 'Otto: Not configured'}
    </div>
  )
}


