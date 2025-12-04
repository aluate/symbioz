'use client'

import { useState, useEffect } from 'react'
import CharacterCreation from '@/components/CharacterCreation'
import HubScreen from '@/components/HubScreen'
import CombatScreen from '@/components/CombatScreen'
import SkillMissionScreen from '@/components/SkillMissionScreen'
import { ErrorBoundary } from '@/components/ErrorBoundary'
import { api } from '@/lib/api'

type Screen = 'character_creation' | 'hub' | 'combat' | 'skill_mission'

export default function Home() {
  const [screen, setScreen] = useState<Screen>('character_creation')
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
      <main style={{ minHeight: '100vh', padding: '20px' }}>
        {screen === 'character_creation' && (
          <CharacterCreation onCharacterCreated={handleCharacterCreated} />
        )}
        {screen === 'hub' && (
          <HubScreen onStartMission={handleStartMission} />
        )}
        {screen === 'combat' && (
          <CombatScreen onCombatEnd={handleCombatEnd} />
        )}
        {screen === 'skill_mission' && currentMission && (
          <SkillMissionScreen
            mission={currentMission.mission}
            skillChecks={currentMission.skill_checks}
            onComplete={handleSkillMissionComplete}
          />
        )}
      </main>
    </ErrorBoundary>
  )
}
