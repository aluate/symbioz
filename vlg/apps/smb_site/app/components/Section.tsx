import styles from './Section.module.css'

interface SectionProps {
  children: React.ReactNode
  title?: string
  subtitle?: string
  variant?: 'default' | 'dark' | 'light' | 'accent'
  className?: string
  id?: string
}

export default function Section({ 
  children, 
  title, 
  subtitle, 
  variant = 'default',
  className = '',
  id
}: SectionProps) {
  const sectionClass = `${styles.section} ${styles[variant]} ${className}`
  
  return (
    <section id={id} className={sectionClass}>
      <div className={styles.container}>
        {(title || subtitle) && (
          <div className={styles.header}>
            {title && <h2 className={styles.title}>{title}</h2>}
            {subtitle && <p className={styles.subtitle}>{subtitle}</p>}
          </div>
        )}
        {children}
      </div>
    </section>
  )
}
