'use client'

import Image from 'next/image'
import styles from './MellivoxLanding.module.css'

interface MellivoxLandingProps {
  onEnter?: () => void
}

export default function MellivoxLanding({ onEnter }: MellivoxLandingProps) {
  const handleEnter = () => {
    if (onEnter) {
      onEnter()
    }
  }

  return (
    <div className={styles.mellivoxLanding}>
      <div className={styles.landingContainer}>
        {/* Logo Section */}
        <div className={styles.logoSection}>
          <Image
            src="/mellivox/mellivox-logo.png"
            alt="Mellivox"
            width={200}
            height={200}
            priority
            className={styles.logo}
          />
        </div>

        {/* Main Content */}
        <div className={styles.contentSection}>
          <h1 className={styles.brandName}>MELLIVOX</h1>
          <p className={styles.tagline}>Honeyvoice of the Pact</p>
          
          <div className={styles.divider}></div>

          <p className={styles.coreTheme}>
            Symbiosis produces consequence.
            <br />
            Every connection changes reality.
          </p>

          <div className={styles.mantras}>
            <p className={styles.mantra}>"The Hive remembers."</p>
            <p className={styles.mantra}>"Everything that touches, changes."</p>
            <p className={styles.mantra}>"All nectar is borrowed."</p>
          </div>

          <div className={styles.divider}></div>

          <div className={styles.threeTruths}>
            <h2 className={styles.truthsTitle}>The Three Truths</h2>
            <ol className={styles.truthsList}>
              <li>Nothing thrives alone.</li>
              <li>Every exchange leaves a scar.</li>
              <li>The Hive remembers.</li>
            </ol>
          </div>

          <div className={styles.ctaSection}>
            <button 
              className={styles.ctaButton}
              onClick={handleEnter}
            >
              Enter the Hive
            </button>
          </div>
        </div>

        {/* Footer */}
        <footer className={styles.landingFooter}>
          <p className={styles.footerText}>
            The bee is our keeper — not a mascot. A cosmic archivist.
          </p>
        </footer>
      </div>
    </div>
  )
}

