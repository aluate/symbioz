"use client"

import React from 'react'
import { type FloorPlan } from '../../../lib/floorPlans'
import styles from './PricingDisplay.module.css'

interface PricingDisplayProps {
  floorPlan: FloorPlan
}

export default function PricingDisplay({ floorPlan }: PricingDisplayProps) {
  const moduleCount = floorPlan.modules.length
  const roomCount = floorPlan.modules.reduce((sum, mod) => sum + mod.rooms.length, 0)

  return (
    <div className={styles.pricing}>
      <h3 className={styles.pricingTitle}>Plan Summary</h3>
      
      <div className={styles.pricingStats}>
        <div className={styles.statItem}>
          <span className={styles.statLabel}>Modules:</span>
          <span className={styles.statValue}>{moduleCount}</span>
        </div>
        <div className={styles.statItem}>
          <span className={styles.statLabel}>Total Sq Ft:</span>
          <span className={styles.statValue}>
            {floorPlan.totalSqFt.toLocaleString()}
          </span>
        </div>
        <div className={styles.statItem}>
          <span className={styles.statLabel}>Rooms:</span>
          <span className={styles.statValue}>{roomCount}</span>
        </div>
      </div>

      <div className={styles.pricingBreakdown}>
        <div className={styles.breakdownItem}>
          <span className={styles.breakdownLabel}>Base Price:</span>
          <span className={styles.breakdownValue}>
            ${floorPlan.estimatedPrice.toLocaleString()}
          </span>
        </div>
        <div className={styles.breakdownNote}>
          * Estimated base price. Final pricing depends on site conditions, finishes, and customizations.
        </div>
      </div>

      {moduleCount === 0 && (
        <div className={styles.emptyMessage}>
          Add modules and rooms to see pricing
        </div>
      )}
    </div>
  )
}

