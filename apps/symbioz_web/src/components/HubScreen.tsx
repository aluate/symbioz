'use client'

import { useState, useEffect, useCallback, useMemo } from 'react'
import { api, Character, Mission } from '@/lib/api'
import LoadingSpinner from '@/components/LoadingSpinner'
import ErrorMessage from '@/components/ErrorMessage'

interface HubScreenProps {
  onStartMission: (missionId: number) => void
}

interface VendorItem {
  id: number
  name: string
  price: number
  type: string
}

export default function HubScreen({ onStartMission }: HubScreenProps) {
  const [character, setCharacter] = useState<Character | null>(null)
  const [missions, setMissions] = useState<Mission[]>([])
  const [loading, setLoading] = useState(true)
  const [showVendor, setShowVendor] = useState(false)
  const [vendorItems, setVendorItems] = useState<VendorItem[]>([])
  const [vendorLoading, setVendorLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    loadData()
  }, [])

  const loadData = useCallback(async () => {
    try {
      setError(null)
      const [charData, missionsData] = await Promise.all([
        api.getCharacter(),
        api.getMissions()
      ])
      setCharacter(charData)
      setMissions(missionsData)
      setLoading(false)
    } catch (error: any) {
      console.error('Failed to load data:', error)
      setError(error.message || 'Failed to load hub data')
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    loadData()
  }, [loadData])

  const handleRest = async () => {
    try {
      const updated = await api.rest()
      setCharacter(updated)
      alert('You rest and recover to full HP!')
    } catch (error: any) {
      alert(error.message || 'Failed to rest')
    }
  }, [])

  const loadVendorItems = useCallback(async () => {
    if (showVendor && vendorItems.length === 0) {
      setVendorLoading(true)
      try {
        const data = await api.getVendorItems()
        setVendorItems(data.items)
      } catch (error: any) {
        console.error('Failed to load vendor items:', error)
        alert(error.message || 'Failed to load vendor')
      } finally {
        setVendorLoading(false)
      }
    }
  }, [showVendor, vendorItems.length])

  useEffect(() => {
    if (showVendor) {
      loadVendorItems()
    }
  }, [showVendor, loadVendorItems])

  const handlePurchase = useCallback(async (itemId: number) => {
    try {
      const updated = await api.purchaseItem(itemId)
      setCharacter(updated)
      // Reload vendor items to refresh
      const data = await api.getVendorItems()
      setVendorItems(data.items)
      alert('Purchase successful!')
    } catch (error: any) {
      alert(error.message || 'Failed to purchase item')
    }
  }, [])

  if (loading) {
    return <LoadingSpinner message="Loading hub..." />
  }

  if (error) {
    return (
      <ErrorMessage
        message={error}
        onRetry={loadData}
        onDismiss={() => setError(null)}
      />
    )
  }

  if (!character) {
    return (
      <div style={{ textAlign: 'center', padding: '40px' }}>
        <p>No character found</p>
      </div>
    )
  }

  return (
    <div style={{
      maxWidth: '1200px',
      margin: '0 auto',
      padding: '20px'
    }}>
      <h1 style={{ fontSize: '2rem', marginBottom: '30px', textAlign: 'center' }}>
        The Outpost
      </h1>

      <div style={{
        display: 'grid',
        gridTemplateColumns: '1fr 2fr',
        gap: '20px',
        marginBottom: '20px'
      }}>
        {/* Character Info */}
        <div style={{
          background: '#1a1a1a',
          border: '2px solid #333',
          borderRadius: '8px',
          padding: '20px'
        }}>
          <h2 style={{ marginBottom: '15px' }}>Character</h2>
          <div style={{ marginBottom: '10px' }}>
            <strong>{character.name}</strong>
          </div>
          <div style={{ marginBottom: '10px', color: '#aaa' }}>
            Level {character.level} {character.race} {character.class}
          </div>
          <div style={{ marginBottom: '10px' }}>
            HP: {character.hp} / {character.maxHp}
          </div>
          <div style={{ marginBottom: '10px' }}>
            Credits: {character.credits}
          </div>
          <div style={{ marginBottom: '10px' }}>
            XP: {character.xp}
          </div>
          <div style={{ marginTop: '15px', paddingTop: '15px', borderTop: '1px solid #333' }}>
            <div style={{ fontSize: '0.9rem', color: '#aaa' }}>
              <div>STR: {character.attributes.STR}</div>
              <div>DEX: {character.attributes.DEX}</div>
              <div>CON: {character.attributes.CON}</div>
              <div>INT: {character.attributes.INT}</div>
            </div>
          </div>
        </div>

        {/* Missions */}
        <div style={{
          background: '#1a1a1a',
          border: '2px solid #333',
          borderRadius: '8px',
          padding: '20px'
        }}>
          <h2 style={{ marginBottom: '15px' }}>Available Missions</h2>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {missions.map((mission) => (
              <button
                key={mission.id}
                onClick={() => onStartMission(mission.id)}
                style={{
                  padding: '15px',
                  background: '#2a2a2a',
                  border: '2px solid #444',
                  borderRadius: '4px',
                  color: '#fff',
                  cursor: 'pointer',
                  textAlign: 'left'
                }}
              >
                <div style={{ fontWeight: 'bold', marginBottom: '5px' }}>{mission.name}</div>
                <div style={{ fontSize: '0.9rem', color: '#aaa', marginBottom: '5px' }}>
                  {mission.description}
                </div>
                <div style={{ fontSize: '0.85rem', color: '#888' }}>
                  XP Reward: {mission.xp_reward} | Type: {mission.type}
                </div>
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Actions */}
      <div style={{
        display: 'flex',
        gap: '15px',
        justifyContent: 'center'
      }}>
        <button
          onClick={() => setShowVendor(!showVendor)}
          style={{
            padding: '12px 24px',
            background: '#3b82f6',
            color: 'white',
            border: 'none',
            borderRadius: '6px',
            cursor: 'pointer',
            fontWeight: 'bold'
          }}
        >
          {showVendor ? 'Hide Vendor' : 'Visit Vendor'}
        </button>
        <button
          onClick={handleRest}
          style={{
            padding: '12px 24px',
            background: '#10b981',
            color: 'white',
            border: 'none',
            borderRadius: '6px',
            cursor: 'pointer',
            fontWeight: 'bold'
          }}
        >
          Rest & Recover
        </button>
      </div>

      {showVendor && (
        <div style={{
          marginTop: '20px',
          background: '#1a1a1a',
          border: '2px solid #333',
          borderRadius: '8px',
          padding: '20px'
        }}>
          <h3 style={{ marginBottom: '15px' }}>Vendor</h3>
          <p style={{ marginBottom: '15px', color: '#aaa' }}>
            Your Credits: <strong style={{ color: '#4ade80' }}>{character?.credits || 0}</strong>
          </p>
          
          {vendorLoading ? (
            <p style={{ color: '#aaa' }}>Loading items...</p>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
              {vendorItems.map((item) => {
                const canAfford = character && character.credits >= item.price
                const itemTypeColors: Record<string, string> = {
                  weapon: '#ef4444',
                  armor: '#6366f1',
                  item: '#10b981'
                }
                const itemColor = itemTypeColors[item.type] || '#666'
                
                return (
                  <div
                    key={item.id}
                    style={{
                      padding: '15px',
                      background: '#2a2a2a',
                      border: `2px solid ${canAfford ? itemColor : '#666'}`,
                      borderRadius: '4px',
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center'
                    }}
                  >
                    <div>
                      <div style={{ fontWeight: 'bold', marginBottom: '5px' }}>{item.name}</div>
                      <div style={{ fontSize: '0.9rem', color: '#aaa' }}>
                        Type: {item.type} | Price: {item.price} credits
                      </div>
                    </div>
                    <button
                      onClick={() => handlePurchase(item.id)}
                      disabled={!canAfford}
                      style={{
                        padding: '8px 16px',
                        background: canAfford ? itemColor : '#666',
                        color: 'white',
                        border: 'none',
                        borderRadius: '4px',
                        cursor: canAfford ? 'pointer' : 'not-allowed',
                        fontWeight: 'bold'
                      }}
                    >
                      {canAfford ? 'Buy' : 'Cannot Afford'}
                    </button>
                  </div>
                )
              })}
            </div>
          )}
          
          {character && character.inventory && character.inventory.length > 0 && (
            <div style={{ marginTop: '20px', paddingTop: '20px', borderTop: '1px solid #333' }}>
              <h4 style={{ marginBottom: '10px' }}>Inventory</h4>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                {character.inventory.map((item, idx) => (
                  <span
                    key={idx}
                    style={{
                      padding: '6px 12px',
                      background: '#2a2a2a',
                      border: '1px solid #444',
                      borderRadius: '4px',
                      fontSize: '0.9rem'
                    }}
                  >
                    {item}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

