"use client"

import React from 'react'
import styles from './FloorFilter.module.css'

export type FloorFilter = 'all' | '1' | '2'

interface FloorFilterProps {
  value: FloorFilter
  onChange: (value: FloorFilter) => void
}

export default function FloorFilter({ value, onChange }: FloorFilterProps) {
  return (
    <div className={styles.filterContainer}>
      <h4 className={styles.filterTitle}>Filter by Floor</h4>
      <div className={styles.filterButtons}>
        <button
          className={`${styles.filterButton} ${value === 'all' ? styles.active : ''}`}
          onClick={() => onChange('all')}
        >
          All Floors
        </button>
        <button
          className={`${styles.filterButton} ${value === '1' ? styles.active : ''}`}
          onClick={() => onChange('1')}
        >
          Level 1
        </button>
        <button
          className={`${styles.filterButton} ${value === '2' ? styles.active : ''}`}
          onClick={() => onChange('2')}
        >
          Level 2
        </button>
      </div>
    </div>
  )
}

