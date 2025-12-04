'use client'

import { useState, useEffect } from 'react'
import { api, Character } from '@/lib/api'

interface SkillCheck {
  attribute: string
  dc: number
  description: string
}

interface SkillMissionScreenProps {
  mission: any
  skillChecks: SkillCheck[]
  onComplete: (result: any) => void
}

export default function SkillMissionScreen({ mission, skillChecks, onComplete }: SkillMissionScreenProps) {
  const [character, setCharacter] = useState<Character | null>(null)
  const [currentCheckIndex, setCurrentCheckIndex] = useState(0)
  const [checkResults, setCheckResults] = useState<Array<{ passed: boolean; total: number; dc: number }>>([])
  const [rolling, setRolling] = useState(false)
  const [missionComplete, setMissionComplete] = useState(false)

  useEffect(() => {
    loadCharacter()
  }, [])

  const loadCharacter = async () => {
    try {
      const char = await api.getCharacter()
      setCharacter(char)
    } catch (error) {
      console.error('Failed to load character:', error)
    }
  }

  const handleRoll = async () => {
    if (currentCheckIndex >= skillChecks.length) return

    setRolling(true)
    const check = skillChecks[currentCheckIndex]
    
    try {
      const result = await api.skillCheck(check.attribute, check.dc)
      setCheckResults(prev => [...prev, result])
      
      if (result.passed) {
        // Move to next check
        if (currentCheckIndex < skillChecks.length - 1) {
          setCurrentCheckIndex(prev => prev + 1)
        } else {
          // All checks passed
          await handleMissionComplete(true)
        }
      } else {
        // Failed check - mission failed
        await handleMissionComplete(false)
      }
    } catch (error: any) {
      alert(error.message || 'Failed to roll skill check')
    } finally {
      setRolling(false)
    }
  }

  const handleMissionComplete = async (success: boolean) => {
    try {
      const result = await api.completeSkillMission(success)
      setMissionComplete(true)
      setTimeout(() => {
        onComplete(result)
      }, 3000)
    } catch (error: any) {
      alert(error.message || 'Failed to complete mission')
    }
  }

  if (!character) {
    return (
      <div style={{ textAlign: 'center', padding: '40px' }}>
        <p>Loading...</p>
      </div>
    )
  }

  if (missionComplete) {
    const lastResult = checkResults[checkResults.length - 1]
    const allPassed = checkResults.every(r => r.passed)
    
    return (
      <div style={{
        maxWidth: '800px',
        margin: '0 auto',
        padding: '40px',
        background: '#1a1a1a',
        borderRadius: '8px',
        border: '2px solid #333',
        textAlign: 'center'
      }}>
        <h1 style={{ fontSize: '2rem', marginBottom: '20px', color: allPassed ? '#4ade80' : '#ef4444' }}>
          {allPassed ? 'Mission Success!' : 'Mission Failed'}
        </h1>
        <p style={{ color: '#aaa', marginBottom: '30px' }}>
          {allPassed 
            ? 'You completed all skill checks successfully!'
            : 'You failed a skill check. Mission incomplete.'}
        </p>
        <p style={{ color: '#888' }}>Returning to hub...</p>
      </div>
    )
  }

  const currentCheck = skillChecks[currentCheckIndex]
  const attributeValue = character.attributes[currentCheck.attribute as keyof typeof character.attributes]
  const attributeMod = Math.floor((attributeValue - 10) / 2)

  return (
    <div style={{
      maxWidth: '800px',
      margin: '0 auto',
      padding: '40px',
      background: '#1a1a1a',
      borderRadius: '8px',
      border: '2px solid #333'
    }}>
      <h1 style={{ fontSize: '2rem', marginBottom: '10px' }}>{mission.name}</h1>
      <p style={{ color: '#aaa', marginBottom: '30px' }}>{mission.description}</p>

      <div style={{
        background: '#2a2a2a',
        border: '1px solid #444',
        borderRadius: '4px',
        padding: '20px',
        marginBottom: '20px'
      }}>
        <h2 style={{ marginBottom: '15px' }}>Progress</h2>
        <div style={{ display: 'flex', gap: '10px', marginBottom: '20px' }}>
          {skillChecks.map((_, idx) => (
            <div
              key={idx}
              style={{
                flex: 1,
                height: '8px',
                background: idx < currentCheckIndex 
                  ? (checkResults[idx]?.passed ? '#4ade80' : '#ef4444')
                  : idx === currentCheckIndex 
                  ? '#3b82f6' 
                  : '#444',
                borderRadius: '4px'
              }}
            />
          ))}
        </div>
        <div style={{ fontSize: '0.9rem', color: '#aaa' }}>
          Check {currentCheckIndex + 1} of {skillChecks.length}
        </div>
      </div>

      {currentCheck && (
        <div style={{
          background: '#2a2a2a',
          border: '2px solid #3b82f6',
          borderRadius: '8px',
          padding: '30px',
          marginBottom: '20px',
          textAlign: 'center'
        }}>
          <h2 style={{ marginBottom: '15px' }}>Current Skill Check</h2>
          <p style={{ fontSize: '1.2rem', marginBottom: '20px', color: '#ccc' }}>
            {currentCheck.description}
          </p>
          <div style={{
            display: 'flex',
            justifyContent: 'center',
            gap: '30px',
            marginBottom: '20px',
            fontSize: '0.9rem',
            color: '#aaa'
          }}>
            <div>
              <strong>Attribute:</strong> {currentCheck.attribute}
            </div>
            <div>
              <strong>Your {currentCheck.attribute}:</strong> {attributeValue} ({attributeMod >= 0 ? '+' : ''}{attributeMod})
            </div>
            <div>
              <strong>Difficulty:</strong> DC {currentCheck.dc}
            </div>
          </div>
          <button
            onClick={handleRoll}
            disabled={rolling}
            style={{
              padding: '15px 30px',
              fontSize: '1.1rem',
              background: rolling ? '#666' : '#3b82f6',
              color: 'white',
              border: 'none',
              borderRadius: '6px',
              cursor: rolling ? 'not-allowed' : 'pointer',
              fontWeight: 'bold'
            }}
          >
            {rolling ? 'Rolling...' : 'Roll Skill Check'}
          </button>
        </div>
      )}

      {checkResults.length > 0 && (
        <div style={{
          background: '#2a2a2a',
          border: '1px solid #444',
          borderRadius: '4px',
          padding: '20px'
        }}>
          <h3 style={{ marginBottom: '15px' }}>Check Results</h3>
          {checkResults.map((result, idx) => (
            <div
              key={idx}
              style={{
                padding: '10px',
                marginBottom: '10px',
                background: result.passed ? '#1a3a1a' : '#3a1a1a',
                border: `1px solid ${result.passed ? '#4ade80' : '#ef4444'}`,
                borderRadius: '4px'
              }}
            >
              <div style={{ fontWeight: 'bold', marginBottom: '5px' }}>
                {skillChecks[idx].description}
              </div>
              <div style={{ fontSize: '0.9rem', color: '#aaa' }}>
                Rolled: <strong style={{ color: result.passed ? '#4ade80' : '#ef4444' }}>
                  {result.total}
                </strong> (DC {result.dc}) - {result.passed ? 'Success!' : 'Failure!'}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

