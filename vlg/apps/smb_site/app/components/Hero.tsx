import Button from './Button'
import styles from './Hero.module.css'

export default function Hero() {
  return (
    <section className={styles.hero}>
      <div className={styles.container}>
        <div className={styles.content}>
          <h1 className={styles.headline}>
            Mountain-Modern Homes, Built with Precision.
          </h1>
          <p className={styles.subheadline}>
            Full-service construction, modular installs, and spec development for mountain and lake country living across the Inland Northwest.
          </p>
          <div className={styles.ctaGroup}>
            <Button href="/contact" variant="primary">
              Schedule a Consultation
            </Button>
            <Button href="/our-homes" variant="secondary">
              View Recent Projects
            </Button>
          </div>
        </div>
      </div>
    </section>
  )
}
