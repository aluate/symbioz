import Section from '../components/Section'
import Button from '../components/Button'

export default function RemodelsAdditions() {
  return (
    <>
      <Section
        title="Make the Home You Have Feel Like the One You Want."
        subtitle="Kitchens, additions, whole-house refreshes, and 'this place needs to actually work for us now' remodels. We bring the same planning and schedule discipline to remodels that we do to new construction."
        variant="default"
      >
        <div style={{ 
          maxWidth: '800px', 
          margin: '2rem auto 0',
          fontFamily: 'var(--font-inter)',
          fontSize: '1.125rem',
          lineHeight: '1.8',
          color: 'var(--color-charcoal)'
        }}>
          <p style={{ marginBottom: '2rem' }}>
            Whether you're looking to update a single room or transform your entire home, we approach every remodel with the same attention to detail and schedule management that defines our new construction work.
          </p>
          
          <div style={{ 
            display: 'grid',
            gridTemplateColumns: '1fr',
            gap: '2rem',
            marginTop: '2rem'
          }}>
            <div>
              <h3 style={{ 
                fontFamily: 'var(--font-playfair)', 
                fontSize: '1.5rem', 
                fontWeight: 700, 
                marginBottom: '0.75rem',
                color: 'var(--color-black)'
              }}>
                Kitchen Remodels
              </h3>
              <p>
                Complete kitchen transformations with modern layouts, quality finishes, and efficient workflows. We work with you to design a kitchen that fits how you actually cook and gather.
              </p>
            </div>
            
            <div>
              <h3 style={{ 
                fontFamily: 'var(--font-playfair)', 
                fontSize: '1.5rem', 
                fontWeight: 700, 
                marginBottom: '0.75rem',
                color: 'var(--color-black)'
              }}>
                Additions
              </h3>
              <p>
                Expand your living space with thoughtful additions that feel like they were always part of the original design. We handle design, permitting, and seamless integration with existing structures.
              </p>
            </div>
            
            <div>
              <h3 style={{ 
                fontFamily: 'var(--font-playfair)', 
                fontSize: '1.5rem', 
                fontWeight: 700, 
                marginBottom: '0.75rem',
                color: 'var(--color-black)'
              }}>
                Whole-House Refreshes
              </h3>
              <p>
                Comprehensive updates throughout your home—new finishes, updated systems, and improved layouts that make your house work better for your lifestyle.
              </p>
            </div>
            
            <div>
              <h3 style={{ 
                fontFamily: 'var(--font-playfair)', 
                fontSize: '1.5rem', 
                fontWeight: 700, 
                marginBottom: '0.75rem',
                color: 'var(--color-black)'
              }}>
                Functional Improvements
              </h3>
              <p>
                Sometimes a home just needs to work better—better storage, better flow, better use of space. We help you identify and execute the changes that make the biggest difference.
              </p>
            </div>
          </div>
          
          <div style={{ 
            marginTop: '3rem',
            padding: '2rem',
            backgroundColor: 'var(--color-warm-white)',
            borderRadius: '4px',
            borderLeft: '4px solid var(--color-tiffany-blue)'
          }}>
            <p style={{ 
              margin: 0,
              fontStyle: 'italic',
              color: 'var(--color-charcoal)'
            }}>
              Every remodel project includes the same clear communication, weekly updates, and schedule management you'd expect from a new build. We minimize disruption and keep you informed every step of the way.
            </p>
          </div>
        </div>
        
        <div style={{ marginTop: '3rem', textAlign: 'center' }}>
          <Button href="/contact" variant="primary">
            Start Your Remodel
          </Button>
        </div>
      </Section>
    </>
  )
}
