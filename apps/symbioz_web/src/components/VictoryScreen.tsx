'use client'

interface VictoryScreenProps {
  result: {
    xp_gained: number
    leveled_up: boolean
    new_level?: number
    credits_gained: number
    items_found: string[]
  }
  onContinue: () => void
}

export default function VictoryScreen({ result, onContinue }: VictoryScreenProps) {
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
        border: '3px solid #4ade80',
        borderRadius: '12px',
        padding: '40px',
        maxWidth: '500px',
        textAlign: 'center'
      }}>
        <h1 style={{ 
          fontSize: '3rem', 
          color: '#4ade80', 
          marginBottom: '20px',
          textShadow: '0 0 20px #4ade80'
        }}>
          VICTORY!
        </h1>
        
        <div style={{ marginBottom: '20px' }}>
          <div style={{ fontSize: '1.2rem', marginBottom: '10px' }}>
            XP Gained: <strong style={{ color: '#3b82f6' }}>{result.xp_gained}</strong>
          </div>
          
          {result.leveled_up && (
            <div style={{
              fontSize: '1.5rem',
              color: '#f59e0b',
              marginBottom: '10px',
              fontWeight: 'bold'
            }}>
              ⭐ LEVEL UP! ⭐
            </div>
          )}
          
          {result.credits_gained > 0 && (
            <div style={{ fontSize: '1.1rem', marginBottom: '10px' }}>
              Credits: <strong style={{ color: '#4ade80' }}>+{result.credits_gained}</strong>
            </div>
          )}
          
          {result.items_found.length > 0 && (
            <div style={{ marginTop: '15px' }}>
              <div style={{ marginBottom: '10px', color: '#aaa' }}>Items Found:</div>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', justifyContent: 'center' }}>
                {result.items_found.map((item, idx) => (
                  <span
                    key={idx}
                    style={{
                      padding: '6px 12px',
                      background: '#2a2a2a',
                      border: '1px solid #4ade80',
                      borderRadius: '4px',
                      color: '#4ade80'
                    }}
                  >
                    {item}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
        
        <button
          onClick={onContinue}
          style={{
            padding: '15px 30px',
            fontSize: '1.1rem',
            background: '#4ade80',
            color: '#000',
            border: 'none',
            borderRadius: '6px',
            cursor: 'pointer',
            fontWeight: 'bold'
          }}
        >
          Continue
        </button>
      </div>
    </div>
  )
}

