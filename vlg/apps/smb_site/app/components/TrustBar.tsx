import styles from './TrustBar.module.css'

export default function TrustBar() {
  return (
    <section className={styles.trustBar}>
      <div className={styles.container}>
        <h2 className={styles.heading}>
          Built for the way you actually live in the mountains.
        </h2>
        <p className={styles.description}>
          From snow loads to steep drives, frozen hose bibs to wildfire risk, Sugar Mountain Builders designs and builds homes that are beautiful, durable, and tuned to real mountain life—not just the brochure version.
        </p>
      </div>
    </section>
  )
}
