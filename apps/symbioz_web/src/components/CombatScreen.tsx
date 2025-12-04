'use client'

import { useState, useEffect, useMemo, useCallback } from 'react'
import { api, CombatState, Enemy } from '@/lib/api'
import LoadingSpinner from '@/components/LoadingSpinner'
import ErrorMessage from '@/components/ErrorMessage'
import VictoryScreen from '@/components/VictoryScreen'
import DefeatScreen from '@/components/DefeatScreen'

interface CombatScreenProps {
  onCombatEnd?: (result: any) => void
}

export default function CombatScreen({ onCombatEnd }: CombatScreenProps) {
  const [combatState, setCombatState] = useState<CombatState | null>(null)
  const [combatLog, setCombatLog] = useState<string[]>(['Combat begins!'])
  const [loading, setLoading] = useState(true)
  const [actionLoading, setActionLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [victoryResult, setVictoryResult] = useState<any>(null)
  const [defeated, setDefeated] = useState(false)
  const [showAbilityMenu, setShowAbilityMenu] = useState(false)
  const [showItemMenu, setShowItemMenu] = useState(false)
  const [showTargetMenu, setShowTargetMenu] = useState(false)
  const [pendingAction, setPendingAction] = useState<{ type: string; ability?: string; item?: string } | null>(null)

  useEffect(() => {
    loadCombatState()
  }, []) // eslint-disable-line react-hooks/exhaustive-deps

  const loadCombatStateMemo = useCallback(loadCombatState, [])

  const loadCombatState = async () => {
    try {
      setError(null)
      const state = await api.getCombatState()
      setCombatState(state)
      setLoading(false)
    } catch (error: any) {
      console.error('Failed to load combat state:', error)
      setError(error.message || 'Failed to load combat state')
      setLoading(false)
    }
  }

  const handleAction = async (actionType: string) => {
    if (actionLoading || !combatState?.is_player_turn) return

    if (actionType === 'ability') {
      setShowAbilityMenu(true)
      setPendingAction({ type: 'ability' })
      return
    }

    if (actionType === 'item') {
      if (!combatState.player.inventory || combatState.player.inventory.length === 0) {
        alert('You have no items!')
        return
      }
      setShowItemMenu(true)
      setPendingAction({ type: 'item' })
      return
    }

    if (actionType === 'attack') {
      if (!combatState.enemies || combatState.enemies.length === 0) {
        alert('No enemies to attack!')
        return
      }
      if (combatState.enemies.length === 1) {
        // Auto-target if only one enemy
        await executeAction(actionType, 0)
      } else {
        setShowTargetMenu(true)
        setPendingAction({ type: 'attack' })
      }
      return
    }

    // Defend or other direct actions
    await executeAction(actionType)
  }

  const handleAbilitySelect = (abilityName: string) => {
    setShowAbilityMenu(false)
    const needsTarget = ['Hack', 'Overload Systems'].includes(abilityName)
    
    if (needsTarget && combatState && combatState.enemies.length > 0) {
      setShowTargetMenu(true)
      setPendingAction({ type: 'ability', ability: abilityName })
    } else {
      executeAction('ability', undefined, abilityName)
    }
  }

  const handleItemSelect = (itemName: string) => {
    setShowItemMenu(false)
    executeAction('item', undefined, undefined, itemName)
  }

  const handleTargetSelect = async (targetId: number) => {
    setShowTargetMenu(false)
    if (pendingAction) {
      if (pendingAction.type === 'attack') {
        await executeAction('attack', targetId)
      } else if (pendingAction.type === 'ability' && pendingAction.ability) {
        await executeAction('ability', targetId, pendingAction.ability)
      }
      setPendingAction(null)
    }
  }

  const executeAction = useCallback(async (
    actionType: string,
    targetId?: number,
    abilityName?: string,
    itemName?: string
  ) => {
    setActionLoading(true)
    try {
      const result = await api.combatAction(actionType, targetId, abilityName, itemName)
      
      // Add combat log entries
      if (result.combat_log) {
        setCombatLog(prev => [...prev, ...result.combat_log])
      }

      // Check if combat ended
      if (result.status === 'victory') {
        setVictoryResult(result)
      } else if (result.status === 'defeat') {
        setDefeated(true)
      } else {
        // Update combat state
        if (result.combat_state) {
          setCombatState(result.combat_state)
        } else {
          await loadCombatStateMemo()
        }
      }
    } catch (error: any) {
      console.error('Action failed:', error)
      setError(error.message || 'Action failed')
      setActionLoading(false)
    }
  }, [loadCombatStateMemo])

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '40px' }}>
        <p>Loading combat...</p>
      </div>
    )
  }

  if (!combatState) {
    return (
      <div style={{ textAlign: 'center', padding: '40px' }}>
        <p>No active combat</p>
      </div>
    )
  }

  const { player, enemies } = combatState

  if (victoryResult) {
    return (
      <VictoryScreen
        result={victoryResult}
        onContinue={() => {
          if (onCombatEnd) {
            onCombatEnd(victoryResult)
          }
        }}
      />
    )
  }

  if (defeated) {
    return (
      <DefeatScreen
        onContinue={() => {
          if (onCombatEnd) {
            onCombatEnd({ status: 'defeat' })
          }
        }}
      />
    )
  }

  return (
    <div style={{
      display: 'grid',
      gridTemplateColumns: '1fr 1fr',
      gridTemplateRows: 'auto 1fr auto',
      gap: '20px',
      maxWidth: '1400px',
      margin: '0 auto',
      minHeight: 'calc(100vh - 40px)'
    }}>
      {/* Header */}
      <div style={{
        gridColumn: '1 / -1',
        textAlign: 'center',
        padding: '20px',
        borderBottom: '2px solid #333'
      }}>
        <h1 style={{ fontSize: '2rem', marginBottom: '10px' }}>SYMBIOZ</h1>
        <p style={{ color: '#888' }}>Combat Screen - Phase 4</p>
        <div style={{ 
          display: 'flex', 
          justifyContent: 'center', 
          alignItems: 'center',
          gap: '20px',
          marginTop: '10px'
        }}>
          {combatState.is_player_turn ? (
            <div style={{
              padding: '8px 16px',
              background: '#4ade80',
              color: '#000',
              borderRadius: '4px',
              fontWeight: 'bold',
              animation: 'pulse 1s infinite'
            }}>
              Your Turn
            </div>
          ) : (
            <div style={{
              padding: '8px 16px',
              background: '#666',
              color: '#fff',
              borderRadius: '4px'
            }}>
              {combatState.current_actor}'s Turn
            </div>
          )}
          <div style={{ fontSize: '0.9rem', color: '#888' }}>
            Round {combatState.round}
          </div>
        </div>
      </div>

      {/* Player Panel */}
      <div style={{
        background: '#1a1a1a',
        border: '2px solid #333',
        borderRadius: '8px',
        padding: '20px',
        display: 'flex',
        flexDirection: 'column',
        gap: '15px'
      }}>
        <div style={{ textAlign: 'center' }}>
          <div style={{
            width: '200px',
            height: '200px',
            background: '#2a2a2a',
            border: '2px solid #444',
            borderRadius: '8px',
            margin: '0 auto 15px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#666',
            fontSize: '0.9rem'
          }}>
            <div style={{ textAlign: 'center' }}>
              <div>Player Portrait</div>
              <div style={{ fontSize: '0.7rem', marginTop: '5px' }}>
                {player.race} {player.class}
              </div>
            </div>
          </div>
          <h2 style={{ fontSize: '1.5rem', marginBottom: '5px' }}>
            {player.name}
          </h2>
          <p style={{ color: '#888', fontSize: '0.9rem' }}>
            Level {player.level} {player.class}
          </p>
        </div>

        <div style={{ borderTop: '1px solid #333', paddingTop: '15px' }}>
          <div style={{ marginBottom: '10px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '5px' }}>
              <span>HP:</span>
              <span style={{ color: '#4ade80' }}>
                {player.hp} / {player.maxHp}
              </span>
            </div>
            <div style={{
              width: '100%',
              height: '20px',
              background: '#2a2a2a',
              borderRadius: '4px',
              overflow: 'hidden'
            }}>
              <div style={{
                width: `${(player.hp / player.maxHp) * 100}%`,
                height: '100%',
                background: '#4ade80',
                transition: 'width 0.3s'
              }} />
            </div>
          </div>

          <div style={{ fontSize: '0.85rem', color: '#aaa', marginTop: '15px' }}>
            <div><strong>STR:</strong> {player.attributes.STR}</div>
            <div><strong>DEX:</strong> {player.attributes.DEX}</div>
            <div><strong>CON:</strong> {player.attributes.CON}</div>
            <div><strong>INT:</strong> {player.attributes.INT}</div>
          </div>
        </div>
      </div>

      {/* Enemy Panel */}
      <div style={{
        background: '#1a1a1a',
        border: '2px solid #333',
        borderRadius: '8px',
        padding: '20px',
        display: 'flex',
        flexDirection: 'column',
        gap: '15px',
        overflowY: 'auto',
        maxHeight: 'calc(100vh - 300px)'
      }}>
        {enemies.length > 0 ? (
          <div style={{
            display: 'grid',
            gridTemplateColumns: enemies.length === 1 ? '1fr' : 'repeat(auto-fit, minmax(250px, 1fr))',
            gap: '15px'
          }}>
            {enemies.map((enemy, idx) => {
              const hpPercent = (enemy.hp / enemy.maxHp) * 100
              const isLowHp = hpPercent < 30
              const isCritical = hpPercent < 15
              
              return (
                <div
                  key={idx}
                  style={{
                    background: '#2a2a2a',
                    border: '2px solid #444',
                    borderRadius: '8px',
                    padding: '15px',
                    position: 'relative'
                  }}
                >
                  {/* Turn Indicator */}
                  {combatState.current_actor === enemy.name && (
                    <div style={{
                      position: 'absolute',
                      top: '10px',
                      right: '10px',
                      width: '12px',
                      height: '12px',
                      background: '#3b82f6',
                      borderRadius: '50%',
                      animation: 'pulse 1s infinite',
                      boxShadow: '0 0 10px #3b82f6'
                    }} />
                  )}
                  
                  <div style={{ textAlign: 'center', marginBottom: '15px' }}>
                    <div style={{
                      width: '120px',
                      height: '120px',
                      background: '#1a1a1a',
                      border: `2px solid ${isCritical ? '#ef4444' : '#444'}`,
                      borderRadius: '8px',
                      margin: '0 auto 10px',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      color: '#666',
                      fontSize: '0.8rem'
                    }}>
                      <div style={{ textAlign: 'center' }}>
                        <div>Enemy</div>
                        <div style={{ fontSize: '0.7rem', marginTop: '5px' }}>
                          {enemy.name}
                        </div>
                      </div>
                    </div>
                    <h3 style={{ 
                      fontSize: '1.2rem', 
                      marginBottom: '5px', 
                      color: isCritical ? '#ef4444' : '#fff'
                    }}>
                      {enemy.name}
                    </h3>
                    <p style={{ color: '#888', fontSize: '0.85rem' }}>
                      Level {enemy.level}
                    </p>
                  </div>

                  <div style={{ borderTop: '1px solid #333', paddingTop: '15px' }}>
                    <div style={{ marginBottom: '10px' }}>
                      <div style={{ 
                        display: 'flex', 
                        justifyContent: 'space-between', 
                        marginBottom: '5px',
                        fontSize: '0.9rem'
                      }}>
                        <span>HP:</span>
                        <span style={{ 
                          color: isCritical ? '#ef4444' : isLowHp ? '#f59e0b' : '#ef4444',
                          fontWeight: isCritical ? 'bold' : 'normal'
                        }}>
                          {enemy.hp} / {enemy.maxHp}
                        </span>
                      </div>
                      <div style={{
                        width: '100%',
                        height: '16px',
                        background: '#1a1a1a',
                        borderRadius: '4px',
                        overflow: 'hidden',
                        border: '1px solid #333'
                      }}>
                        <div style={{
                          width: `${hpPercent}%`,
                          height: '100%',
                          background: isCritical ? '#ef4444' : isLowHp ? '#f59e0b' : '#ef4444',
                          transition: 'width 0.3s, background 0.3s',
                          boxShadow: isCritical ? '0 0 10px #ef4444' : 'none'
                        }} />
                      </div>
                    </div>
                    
                    {/* Status Effects Placeholder */}
                    {combatState.player.status_effects && combatState.player.status_effects.length > 0 && (
                      <div style={{ 
                        fontSize: '0.75rem', 
                        color: '#888',
                        marginTop: '10px',
                        paddingTop: '10px',
                        borderTop: '1px solid #333'
                      }}>
                        Status: {combatState.player.status_effects.join(', ')}
                      </div>
                    )}
                  </div>
                </div>
              )
            })}
          </div>
        ) : (
          <div style={{ textAlign: 'center', padding: '40px' }}>
            <p style={{ color: '#4ade80', fontSize: '1.2rem' }}>All enemies defeated!</p>
          </div>
        )}
      </div>

      {/* Combat Log */}
      <div style={{
        gridColumn: '1 / -1',
        background: '#1a1a1a',
        border: '2px solid #333',
        borderRadius: '8px',
        padding: '20px',
        maxHeight: '200px',
        overflowY: 'auto'
      }}>
        <h3 style={{ marginBottom: '10px', fontSize: '1.1rem' }}>Combat Log</h3>
        <div 
          ref={(el) => {
            if (el) el.scrollTop = el.scrollHeight
          }}
          style={{ 
            fontFamily: 'monospace', 
            fontSize: '0.9rem', 
            lineHeight: '1.6',
            maxHeight: '150px',
            overflowY: 'auto'
          }}
        >
          {combatLog.map((log, idx) => {
            const isDamage = log.includes('damage')
            const isDefeat = log.includes('defeated')
            const isSuccess = log.includes('hits') || log.includes('Success')
            
            return (
              <div 
                key={idx} 
                style={{ 
                  marginBottom: '5px', 
                  color: isDefeat ? '#4ade80' : isDamage ? '#f59e0b' : isSuccess ? '#3b82f6' : '#ccc',
                  padding: '4px 0',
                  borderLeft: isDefeat ? '3px solid #4ade80' : isDamage ? '3px solid #f59e0b' : 'none',
                  paddingLeft: (isDefeat || isDamage) ? '8px' : '0'
                }}
              >
                {log}
              </div>
            )
          })}
        </div>
      </div>

      {/* Action Buttons */}
      <div style={{
        gridColumn: '1 / -1',
        display: 'flex',
        gap: '15px',
        justifyContent: 'center',
        padding: '20px',
        position: 'relative'
      }}>
        {showAbilityMenu && (
          <div style={{
            position: 'absolute',
            bottom: '80px',
            background: '#2a2a2a',
            border: '2px solid #444',
            borderRadius: '8px',
            padding: '15px',
            zIndex: 1000,
            minWidth: '200px'
          }}>
            <h4 style={{ marginBottom: '10px' }}>Select Ability:</h4>
            {player.abilities.map((ability, idx) => (
              <button
                key={idx}
                onClick={() => handleAbilitySelect(ability)}
                style={{
                  display: 'block',
                  width: '100%',
                  padding: '8px',
                  marginBottom: '5px',
                  background: '#3b82f6',
                  color: 'white',
                  border: 'none',
                  borderRadius: '4px',
                  cursor: 'pointer'
                }}
              >
                {ability}
              </button>
            ))}
            <button
              onClick={() => setShowAbilityMenu(false)}
              style={{
                display: 'block',
                width: '100%',
                padding: '8px',
                marginTop: '10px',
                background: '#666',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer'
              }}
            >
              Cancel
            </button>
          </div>
        )}

        {showItemMenu && (
          <div style={{
            position: 'absolute',
            bottom: '80px',
            background: '#2a2a2a',
            border: '2px solid #444',
            borderRadius: '8px',
            padding: '15px',
            zIndex: 1000,
            minWidth: '200px'
          }}>
            <h4 style={{ marginBottom: '10px' }}>Select Item:</h4>
            {player.inventory.map((item, idx) => (
              <button
                key={idx}
                onClick={() => handleItemSelect(item)}
                style={{
                  display: 'block',
                  width: '100%',
                  padding: '8px',
                  marginBottom: '5px',
                  background: '#10b981',
                  color: 'white',
                  border: 'none',
                  borderRadius: '4px',
                  cursor: 'pointer'
                }}
              >
                {item}
              </button>
            ))}
            <button
              onClick={() => setShowItemMenu(false)}
              style={{
                display: 'block',
                width: '100%',
                padding: '8px',
                marginTop: '10px',
                background: '#666',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer'
              }}
            >
              Cancel
            </button>
          </div>
        )}

        {showTargetMenu && combatState.enemies.length > 0 && (
          <div style={{
            position: 'absolute',
            bottom: '80px',
            background: '#2a2a2a',
            border: '2px solid #444',
            borderRadius: '8px',
            padding: '15px',
            zIndex: 1000,
            minWidth: '200px'
          }}>
            <h4 style={{ marginBottom: '10px' }}>Select Target:</h4>
            {combatState.enemies.map((enemy, idx) => (
              <button
                key={idx}
                onClick={() => handleTargetSelect(idx)}
                style={{
                  display: 'block',
                  width: '100%',
                  padding: '8px',
                  marginBottom: '5px',
                  background: '#ef4444',
                  color: 'white',
                  border: 'none',
                  borderRadius: '4px',
                  cursor: 'pointer'
                }}
              >
                {enemy.name} ({enemy.hp}/{enemy.maxHp} HP)
              </button>
            ))}
            <button
              onClick={() => {
                setShowTargetMenu(false)
                setPendingAction(null)
              }}
              style={{
                display: 'block',
                width: '100%',
                padding: '8px',
                marginTop: '10px',
                background: '#666',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer'
              }}
            >
              Cancel
            </button>
          </div>
        )}

        <button
          onClick={() => handleAction('attack')}
          disabled={actionLoading || !combatState.is_player_turn}
          style={{
            padding: '12px 24px',
            fontSize: '1rem',
            background: combatState.is_player_turn && !actionLoading ? '#ef4444' : '#666',
            color: 'white',
            border: 'none',
            borderRadius: '6px',
            cursor: combatState.is_player_turn && !actionLoading ? 'pointer' : 'not-allowed',
            fontWeight: 'bold',
            transition: 'background 0.2s'
          }}
        >
          Attack
        </button>
        <button
          onClick={() => handleAction('ability')}
          disabled={actionLoading || !combatState.is_player_turn}
          style={{
            padding: '12px 24px',
            fontSize: '1rem',
            background: combatState.is_player_turn && !actionLoading ? '#3b82f6' : '#666',
            color: 'white',
            border: 'none',
            borderRadius: '6px',
            cursor: combatState.is_player_turn && !actionLoading ? 'pointer' : 'not-allowed',
            fontWeight: 'bold',
            transition: 'background 0.2s'
          }}
        >
          Ability
        </button>
        <button
          onClick={() => handleAction('item')}
          disabled={actionLoading || !combatState.is_player_turn}
          style={{
            padding: '12px 24px',
            fontSize: '1rem',
            background: combatState.is_player_turn && !actionLoading ? '#10b981' : '#666',
            color: 'white',
            border: 'none',
            borderRadius: '6px',
            cursor: combatState.is_player_turn && !actionLoading ? 'pointer' : 'not-allowed',
            fontWeight: 'bold',
            transition: 'background 0.2s'
          }}
        >
          Item
        </button>
        <button
          onClick={() => handleAction('defend')}
          disabled={actionLoading || !combatState.is_player_turn}
          style={{
            padding: '12px 24px',
            fontSize: '1rem',
            background: combatState.is_player_turn && !actionLoading ? '#6366f1' : '#666',
            color: 'white',
            border: 'none',
            borderRadius: '6px',
            cursor: combatState.is_player_turn && !actionLoading ? 'pointer' : 'not-allowed',
            fontWeight: 'bold',
            transition: 'background 0.2s'
          }}
        >
          Defend
        </button>
      </div>
    </div>
  )
}
