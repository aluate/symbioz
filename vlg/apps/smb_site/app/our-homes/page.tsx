import Section from '../components/Section'
import ProjectTeaserGrid from '../components/ProjectTeaserGrid'
import Button from '../components/Button'

export default function OurHomes() {
  const projects = [
    {
      title: 'Custom Mountain Home',
      description: 'A full custom home with mountain-modern design, featuring clean lines and thoughtful details.',
      image: '',
    },
    {
      title: 'Spec Development',
      description: 'A spec home project showcasing our proven floor plans and reliable schedules.',
      image: '',
    },
    {
      title: 'Lakefront Retreat',
      description: 'A custom home designed for lake country living with big glass and warm materials.',
      image: '',
    },
  ]
  
  return (
    <>
      <Section
        title="Mountain-Modern, Crafted with Precision."
        subtitle="Homes shaped by the mountains—where clean lines, warm materials, expansive glass, and considered details converge. Every Sugar Mountain home, whether custom or spec-designed, balances sophisticated design, enduring durability, and precise buildability."
        variant="default"
      >
        <div style={{ marginTop: '2rem' }}>
          <h3 style={{ 
            fontFamily: 'var(--font-playfair)', 
            fontSize: '1.75rem', 
            fontWeight: 700, 
            marginBottom: '1rem',
            color: 'var(--color-black)'
          }}>
            Custom & Semi-Custom Homes
          </h3>
          <p style={{ 
            fontFamily: 'var(--font-inter)', 
            fontSize: '1.125rem', 
            lineHeight: '1.7',
            color: 'var(--color-charcoal)',
            marginBottom: '2rem'
          }}>
            From initial concept through final completion, we work alongside you—refining floor plans, curating specifications, selecting finishes, and executing construction. One team, one vision, delivered with certainty.
          </p>
          
          <h3 style={{ 
            fontFamily: 'var(--font-playfair)', 
            fontSize: '1.75rem', 
            fontWeight: 700, 
            marginBottom: '1rem',
            marginTop: '2rem',
            color: 'var(--color-black)'
          }}>
            Spec & Investment Homes
          </h3>
          <p style={{ 
            fontFamily: 'var(--font-inter)', 
            fontSize: '1.125rem', 
            lineHeight: '1.7',
            color: 'var(--color-charcoal)',
            marginBottom: '2rem'
          }}>
            Sugar Mountain Builders also develops spec homes and joint-venture projects. These employ proven floor plans, disciplined budgets, and predictable schedules to deliver exceptional value for investors and future owners.
          </p>
        </div>
        
        <ProjectTeaserGrid projects={projects} />
        
        <div style={{ marginTop: '3rem', textAlign: 'center' }}>
          <Button href="/contact" variant="primary">
            Start Your Project
          </Button>
        </div>
      </Section>
    </>
  )
}
