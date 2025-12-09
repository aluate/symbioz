import styles from './ProcessSteps.module.css'

const steps = [
  {
    number: '1',
    title: 'Intro Call & Site Visit',
    description: 'Understand goals, budget, and site conditions.',
  },
  {
    number: '2',
    title: 'Concept & Rough Budget',
    description: 'Align on scope and ballpark price.',
  },
  {
    number: '3',
    title: 'Plans, Specs, and Final Pricing',
    description: 'Lock the details and schedule.',
  },
  {
    number: '4',
    title: 'Build Phase',
    description: 'Clear communication, weekly updates, decisive problem-solving.',
  },
  {
    number: '5',
    title: 'Walkthrough & Aftercare',
    description: 'Punchlist, warranty, and long-term support.',
  },
]

export default function ProcessSteps() {
  return (
    <div className={styles.processSteps}>
      {steps.map((step, index) => (
        <div key={step.number} className={styles.step}>
          <div className={styles.stepNumber}>{step.number}</div>
          <div className={styles.stepContent}>
            <h3 className={styles.stepTitle}>{step.title}</h3>
            <p className={styles.stepDescription}>{step.description}</p>
          </div>
          {index < steps.length - 1 && <div className={styles.connector}></div>}
        </div>
      ))}
    </div>
  )
}
