'use client'

import { useState, useEffect } from 'react'
import MellivoxLanding from '@/components/MellivoxLanding'
import CharacterCreation from '@/components/CharacterCreation'
import HubScreen from '@/components/HubScreen'
import CombatScreen from '@/components/CombatScreen'
import SkillMissionScreen from '@/components/SkillMissionScreen'
import { ErrorBoundary } from '@/components/ErrorBoundary'
import { api } from '@/lib/api'

type Screen = 'landing' | 'character_creation' | 'hub' | 'combat' | 'skill_mission'

export default function Home() {
  const [screen, setScreen] = useState<Screen>('landing')
  const [hasCharacter, setHasCharacter] = useState(false)
  const [currentMission, setCurrentMission] = useState<any>(null)

  useEffect(() => {
    checkCharacter()
  }, [])

  const checkCharacter = async () => {
    try {
      await api.ensureSession()
      // Try to load existing game
      const hasCharacter = await api.loadGame()
      if (hasCharacter) {
        try {
          const character = await api.getCharacter()
          setHasCharacter(true)
          setScreen('hub')
          return
        } catch (error) {
          // Character load failed, create new
        }
      }
      setHasCharacter(false)
      setScreen('character_creation')
    } catch (error) {
      // No character yet
      setHasCharacter(false)
      setScreen('character_creation')
    }
  }

  const handleCharacterCreated = () => {
    setHasCharacter(true)
    setScreen('hub')
  }

  const handleStartMission = async (missionId: number) => {
    try {
      const result = await api.startMission(missionId)
      if (result.status === 'combat_started') {
        setScreen('combat')
      } else if (result.status === 'mission_started') {
        setCurrentMission(result)
        setScreen('skill_mission')
      } else {
        alert('Unknown mission type')
      }
    } catch (error: any) {
      alert(error.message || 'Failed to start mission')
    }
  }

  const handleSkillMissionComplete = (result: any) => {
    if (result.status === 'success') {
      alert(`Success! XP: ${result.xp_gained}${result.leveled_up ? ' - LEVEL UP!' : ''}`)
    } else {
      alert(`Failed! Reduced XP: ${result.xp_gained}`)
    }
    setCurrentMission(null)
    setScreen('hub')
  }

  const handleCombatEnd = (result: any) => {
    if (result.status === 'victory') {
      alert(`Victory! XP: ${result.xp_gained}${result.leveled_up ? ' - LEVEL UP!' : ''}`)
    } else {
      alert('Defeat! Returning to hub...')
    }
    setScreen('hub')
  }

  return (
    <ErrorBoundary>
      <main style={{ minHeight: '100vh' }}>
        {screen === 'landing' && (
          <MellivoxLanding onEnter={() => {
            // Check if character exists, otherwise go to character creation
            checkCharacter()
          }} />
        )}
        {screen === 'character_creation' && (
          <div style={{ minHeight: '100vh', padding: '20px' }}>
            <CharacterCreation onCharacterCreated={handleCharacterCreated} />
          </div>
        )}
        {screen === 'hub' && (
          <div style={{ minHeight: '100vh', padding: '20px' }}>
            <HubScreen onStartMission={handleStartMission} />
          </div>
        )}
        {screen === 'combat' && (
          <div style={{ minHeight: '100vh', padding: '20px' }}>
            <CombatScreen onCombatEnd={handleCombatEnd} />
          </div>
        )}
        {screen === 'skill_mission' && currentMission && (
          <div style={{ minHeight: '100vh', padding: '20px' }}>
            <SkillMissionScreen
              mission={currentMission.mission}
              skillChecks={currentMission.skill_checks}
              onComplete={handleSkillMissionComplete}
            />
          </div>
        )}
      </main>
    </ErrorBoundary>
  )
}
