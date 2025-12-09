import styles from './ProjectTeaserGrid.module.css'

interface ProjectTeaser {
  title: string
  description: string
  image?: string
}

interface ProjectTeaserGridProps {
  projects: ProjectTeaser[]
}

export default function ProjectTeaserGrid({ projects }: ProjectTeaserGridProps) {
  return (
    <div className={styles.grid}>
      {projects.map((project, index) => (
        <div key={index} className={styles.card}>
          <div className={styles.imagePlaceholder}>
            {/* TODO: Replace with actual project images */}
            <span className={styles.placeholderText}>Project Image</span>
          </div>
          <div className={styles.content}>
            <h3 className={styles.title}>{project.title}</h3>
            <p className={styles.description}>{project.description}</p>
          </div>
        </div>
      ))}
    </div>
  )
}
