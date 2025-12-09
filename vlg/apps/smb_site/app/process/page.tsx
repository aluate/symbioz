import Section from '../components/Section'
import ProcessSteps from '../components/ProcessSteps'
import Button from '../components/Button'

export default function Process() {
  return (
    <>
      <Section
        title="A Straightforward, Five-Phase Process."
        subtitle="From initial conversation to final walkthrough, we follow a clear, structured approach that keeps your project on schedule and on budget."
        variant="default"
      >
        <ProcessSteps />
        
        <div style={{ 
          maxWidth: '800px', 
          margin: '3rem auto 0',
          fontFamily: 'var(--font-inter)',
          fontSize: '1.125rem',
          lineHeight: '1.8',
          color: 'var(--color-charcoal)'
        }}>
          <p>
            Our five-phase process ensures that nothing falls through the cracks. We believe in setting clear expectations from the start, maintaining open communication throughout, and delivering on our promises.
          </p>
          
          <div style={{ 
            marginTop: '2rem',
            padding: '2rem',
            backgroundColor: 'var(--color-black)',
            color: 'white',
            borderRadius: '4px'
          }}>
            <h3 style={{ 
              fontFamily: 'var(--font-playfair)', 
              fontSize: '1.5rem', 
              fontWeight: 700, 
              marginBottom: '1rem',
              color: 'white'
            }}>
              What Makes Our Process Different
            </h3>
            <ul style={{ 
              listStyle: 'none',
              padding: 0,
              margin: 0
            }}>
              <li style={{ 
                padding: '0.5rem 0',
                paddingLeft: '1.5rem',
                position: 'relative'
              }}>
                <span style={{ 
                  position: 'absolute',
                  left: 0,
                  color: 'var(--color-tiffany-blue)'
                }}>•</span>
                Transparent pricing and realistic timelines from day one
              </li>
              <li style={{ 
                padding: '0.5rem 0',
                paddingLeft: '1.5rem',
                position: 'relative'
              }}>
                <span style={{ 
                  position: 'absolute',
                  left: 0,
                  color: 'var(--color-tiffany-blue)'
                }}>•</span>
                Weekly updates so you're never left wondering
              </li>
              <li style={{ 
                padding: '0.5rem 0',
                paddingLeft: '1.5rem',
                position: 'relative'
              }}>
                <span style={{ 
                  position: 'absolute',
                  left: 0,
                  color: 'var(--color-tiffany-blue)'
                }}>•</span>
                Decisions made quickly to keep momentum
              </li>
              <li style={{ 
                padding: '0.5rem 0',
                paddingLeft: '1.5rem',
                position: 'relative'
              }}>
                <span style={{ 
                  position: 'absolute',
                  left: 0,
                  color: 'var(--color-tiffany-blue)'
                }}>•</span>
                Long-term support after completion
              </li>
            </ul>
          </div>
        </div>
        
        <div style={{ marginTop: '3rem', textAlign: 'center' }}>
          <Button href="/contact" variant="primary">
            Start Phase 1: Schedule a Call
          </Button>
        </div>
      </Section>
    </>
  )
}
