'use client'

import { useState, useEffect } from 'react'
import { api, Race, Class } from '@/lib/api'

interface CharacterCreationProps {
  onCharacterCreated: () => void
}

export default function CharacterCreation({ onCharacterCreated }: CharacterCreationProps) {
  const [name, setName] = useState('')
  const [races, setRaces] = useState<Race[]>([])
  const [classes, setClasses] = useState<Class[]>([])
  const [selectedRaceId, setSelectedRaceId] = useState<number | null>(null)
  const [selectedClassId, setSelectedClassId] = useState<number | null>(null)
  const [loading, setLoading] = useState(true)
  const [creating, setCreating] = useState(false)

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      await api.ensureSession()
      const [racesData, classesData] = await Promise.all([
        api.getRaces(),
        api.getClasses()
      ])
      setRaces(racesData)
      setClasses(classesData)
      setLoading(false)
    } catch (error) {
      console.error('Failed to load data:', error)
      setLoading(false)
    }
  }

  const handleCreate = async () => {
    if (!name.trim() || !selectedRaceId || !selectedClassId) {
      alert('Please fill in all fields')
      return
    }

    setCreating(true)
    try {
      await api.createCharacter(name, selectedRaceId, selectedClassId)
      onCharacterCreated()
    } catch (error: any) {
      console.error('Failed to create character:', error)
      alert(error.message || 'Failed to create character')
    } finally {
      setCreating(false)
    }
  }

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '40px' }}>
        <p>Loading...</p>
      </div>
    )
  }

  return (
    <div style={{
      maxWidth: '600px',
      margin: '0 auto',
      padding: '40px',
      background: '#1a1a1a',
      borderRadius: '8px',
      border: '2px solid #333'
    }}>
      <h1 style={{ fontSize: '2rem', marginBottom: '30px', textAlign: 'center' }}>
        Create Your Character
      </h1>

      <div style={{ marginBottom: '20px' }}>
        <label style={{ display: 'block', marginBottom: '8px', color: '#ccc' }}>
          Character Name
        </label>
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          style={{
            width: '100%',
            padding: '10px',
            background: '#2a2a2a',
            border: '1px solid #444',
            borderRadius: '4px',
            color: '#fff',
            fontSize: '1rem'
          }}
          placeholder="Enter your character's name"
        />
      </div>

      <div style={{ marginBottom: '20px' }}>
        <label style={{ display: 'block', marginBottom: '8px', color: '#ccc' }}>
          Race
        </label>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
          {races.map((race) => (
            <button
              key={race.id}
              onClick={() => setSelectedRaceId(race.id)}
              style={{
                padding: '15px',
                background: selectedRaceId === race.id ? '#3b82f6' : '#2a2a2a',
                border: `2px solid ${selectedRaceId === race.id ? '#3b82f6' : '#444'}`,
                borderRadius: '4px',
                color: '#fff',
                cursor: 'pointer',
                textAlign: 'left'
              }}
            >
              <div style={{ fontWeight: 'bold', marginBottom: '5px' }}>{race.name}</div>
              <div style={{ fontSize: '0.9rem', color: '#aaa' }}>{race.description}</div>
            </button>
          ))}
        </div>
      </div>

      <div style={{ marginBottom: '20px' }}>
        <label style={{ display: 'block', marginBottom: '8px', color: '#ccc' }}>
          Class
        </label>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
          {classes.map((clazz) => (
            <button
              key={clazz.id}
              onClick={() => setSelectedClassId(clazz.id)}
              style={{
                padding: '15px',
                background: selectedClassId === clazz.id ? '#3b82f6' : '#2a2a2a',
                border: `2px solid ${selectedClassId === clazz.id ? '#3b82f6' : '#444'}`,
                borderRadius: '4px',
                color: '#fff',
                cursor: 'pointer',
                textAlign: 'left'
              }}
            >
              <div style={{ fontWeight: 'bold', marginBottom: '5px' }}>{clazz.name}</div>
              <div style={{ fontSize: '0.9rem', color: '#aaa', marginBottom: '5px' }}>
                {clazz.description}
              </div>
              <div style={{ fontSize: '0.85rem', color: '#888' }}>
                Abilities: {clazz.abilities.join(', ')}
              </div>
            </button>
          ))}
        </div>
      </div>

      <button
        onClick={handleCreate}
        disabled={creating || !name.trim() || !selectedRaceId || !selectedClassId}
        style={{
          width: '100%',
          padding: '15px',
          background: creating || !name.trim() || !selectedRaceId || !selectedClassId ? '#666' : '#4ade80',
          border: 'none',
          borderRadius: '4px',
          color: '#fff',
          fontSize: '1.1rem',
          fontWeight: 'bold',
          cursor: creating || !name.trim() || !selectedRaceId || !selectedClassId ? 'not-allowed' : 'pointer'
        }}
      >
        {creating ? 'Creating...' : 'Create Character'}
      </button>
    </div>
  )
}

