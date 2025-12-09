'use client'

import Link from 'next/link'
import { useState } from 'react'
import styles from './Navigation.module.css'

const navItems = [
  { label: 'Home', href: '/' },
  { label: 'Our Homes', href: '/our-homes' },
  { label: 'Floor Plans', href: '/floor-plans' },
  { label: 'Modular Installs', href: '/modular-installs' },
  { label: 'Remodels & Additions', href: '/remodels-additions' },
  { label: 'Process', href: '/process' },
  { label: 'About', href: '/about' },
  { label: 'Contact', href: '/contact' },
]

export default function Navigation() {
  const [isOpen, setIsOpen] = useState(false)
  
  return (
    <nav className={styles.nav}>
      <div className={styles.container}>
        <Link href="/" className={styles.logo}>
          Sugar Mountain Builders
        </Link>
        
        <button 
          className={styles.menuToggle}
          onClick={() => setIsOpen(!isOpen)}
          aria-label="Toggle menu"
        >
          <span className={styles.hamburger}></span>
          <span className={styles.hamburger}></span>
          <span className={styles.hamburger}></span>
        </button>
        
        <ul className={`${styles.navList} ${isOpen ? styles.open : ''}`}>
          {navItems.map((item) => (
            <li key={item.href}>
              <Link 
                href={item.href} 
                className={styles.navLink}
                onClick={() => setIsOpen(false)}
              >
                {item.label}
              </Link>
            </li>
          ))}
        </ul>
      </div>
    </nav>
  )
}
