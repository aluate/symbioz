'use client'

interface DefeatScreenProps {
  onContinue: () => void
}

export default function DefeatScreen({ onContinue }: DefeatScreenProps) {
  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      background: 'rgba(0, 0, 0, 0.9)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 2000
    }}>
      <div style={{
        background: '#1a1a1a',
        border: '3px solid #ef4444',
        borderRadius: '12px',
        padding: '40px',
        maxWidth: '500px',
        textAlign: 'center'
      }}>
        <h1 style={{ 
          fontSize: '3rem', 
          color: '#ef4444', 
          marginBottom: '20px',
          textShadow: '0 0 20px #ef4444'
        }}>
          DEFEAT
        </h1>
        
        <p style={{ fontSize: '1.1rem', color: '#aaa', marginBottom: '30px' }}>
          You have been defeated. Returning to hub with 1 HP...
        </p>
        
        <button
          onClick={onContinue}
          style={{
            padding: '15px 30px',
            fontSize: '1.1rem',
            background: '#ef4444',
            color: '#fff',
            border: 'none',
            borderRadius: '6px',
            cursor: 'pointer',
            fontWeight: 'bold'
          }}
        >
          Return to Hub
        </button>
      </div>
    </div>
  )
}

