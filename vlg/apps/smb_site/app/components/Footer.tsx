import Link from 'next/link'
import styles from './Footer.module.css'

export default function Footer() {
  return (
    <footer className={styles.footer}>
      <div className={styles.container}>
        <div className={styles.content}>
          <div className={styles.brand}>
            <h3 className={styles.logo}>Sugar Mountain Builders</h3>
            <p className={styles.tagline}>Mountain-Modern. Built Right.</p>
          </div>
          
          <div className={styles.links}>
            <div className={styles.column}>
              <h4 className={styles.columnTitle}>Services</h4>
              <ul>
                <li><Link href="/our-homes">Our Homes</Link></li>
                <li><Link href="/modular-installs">Modular Installs</Link></li>
                <li><Link href="/remodels-additions">Remodels & Additions</Link></li>
              </ul>
            </div>
            
            <div className={styles.column}>
              <h4 className={styles.columnTitle}>Company</h4>
              <ul>
                <li><Link href="/process">Our Process</Link></li>
                <li><Link href="/about">About</Link></li>
                <li><Link href="/contact">Contact</Link></li>
              </ul>
            </div>
            
            <div className={styles.column}>
              <h4 className={styles.columnTitle}>Partners</h4>
              <ul>
                <li><a href="#" target="_blank" rel="noopener noreferrer">Stax</a></li>
                <li><a href="#" target="_blank" rel="noopener noreferrer">Grid Cabinet Systems</a></li>
              </ul>
            </div>
          </div>
        </div>
        
        <div className={styles.bottom}>
          <p className={styles.serviceArea}>
            Service area: North Idaho and surrounding Inland Northwest regions.
          </p>
          <p className={styles.copyright}>
            © {new Date().getFullYear()} Sugar Mountain Builders. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  )
}
