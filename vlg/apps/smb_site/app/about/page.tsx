import Section from '../components/Section'
import Button from '../components/Button'

export default function About() {
  return (
    <>
      <Section
        title="Who We Are."
        subtitle="Sugar Mountain Builders crafts luxury mountain homes in the Inland Northwest. Where precision engineering meets alpine design, delivered with certainty."
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
            We build homes shaped by the mountains—where modern architecture meets the rhythm of alpine living. Every detail considered. Every finish curated. Every step predictable. Our commitment to craftsmanship, reliability, and clear communication ensures your home works as beautifully in challenging mountain conditions as it does in photographs.
          </p>
          
          <h3 style={{ 
            fontFamily: 'var(--font-playfair)', 
            fontSize: '1.75rem', 
            fontWeight: 700, 
            marginTop: '2rem',
            marginBottom: '1rem',
            color: 'var(--color-black)'
          }}>
            Our Values
          </h3>
          
          <ul style={{ 
            listStyle: 'none',
            padding: 0,
            marginBottom: '2rem'
          }}>
            <li style={{ 
              padding: '1rem 0',
              paddingLeft: '2rem',
              position: 'relative',
              borderBottom: '1px solid rgba(0, 0, 0, 0.1)'
            }}>
              <span style={{ 
                position: 'absolute',
                left: 0,
                color: 'var(--color-tiffany-blue)',
                fontSize: '1.5rem',
                fontWeight: 700
              }}>✓</span>
              <strong style={{ display: 'block', marginBottom: '0.5rem' }}>
                Truth, even when it's inconvenient.
              </strong>
              <span style={{ color: 'var(--color-charcoal)' }}>
                We engage in transparent conversations about budget and timeline from the start. Certainty over surprises.
              </span>
            </li>
            
            <li style={{ 
              padding: '1rem 0',
              paddingLeft: '2rem',
              position: 'relative',
              borderBottom: '1px solid rgba(0, 0, 0, 0.1)'
            }}>
              <span style={{ 
                position: 'absolute',
                left: 0,
                color: 'var(--color-tiffany-blue)',
                fontSize: '1.5rem',
                fontWeight: 700
              }}>✓</span>
              <strong style={{ display: 'block', marginBottom: '0.5rem' }}>
                Protect schedule and budget.
              </strong>
              <span style={{ color: 'var(--color-charcoal)' }}>
                Precision planning, clear communication, and decisive action keep projects on track—on time, on budget, every time.
              </span>
            </li>
            
            <li style={{ 
              padding: '1rem 0',
              paddingLeft: '2rem',
              position: 'relative',
              borderBottom: '1px solid rgba(0, 0, 0, 0.1)'
            }}>
              <span style={{ 
                position: 'absolute',
                left: 0,
                color: 'var(--color-tiffany-blue)',
                fontSize: '1.5rem',
                fontWeight: 700
              }}>✓</span>
              <strong style={{ display: 'block', marginBottom: '0.5rem' }}>
                Design for how you actually live.
              </strong>
              <span style={{ color: 'var(--color-charcoal)' }}>
                Beautiful design and thoughtful functionality harmonize in homes that serve real life in mountain and lake country.
              </span>
            </li>
            
            <li style={{ 
              padding: '1rem 0',
              paddingLeft: '2rem',
              position: 'relative'
            }}>
              <span style={{ 
                position: 'absolute',
                left: 0,
                color: 'var(--color-tiffany-blue)',
                fontSize: '1.5rem',
                fontWeight: 700
              }}>✓</span>
              <strong style={{ display: 'block', marginBottom: '0.5rem' }}>
                Build like we return every winter.
              </strong>
              <span style={{ color: 'var(--color-charcoal)' }}>
                We craft with the certainty that these homes will endure—through winter storms, spring thaws, and decades of mountain living. Quality is non-negotiable.
              </span>
            </li>
          </ul>
          
          <div style={{ 
            marginTop: '3rem',
            padding: '2rem',
            backgroundColor: 'var(--color-warm-white)',
            borderRadius: '4px'
          }}>
            <h3 style={{ 
              fontFamily: 'var(--font-playfair)', 
              fontSize: '1.5rem', 
              fontWeight: 700, 
              marginBottom: '1rem',
              color: 'var(--color-black)'
            }}>
              Service Area
            </h3>
            <p style={{ 
              margin: 0,
              color: 'var(--color-charcoal)'
            }}>
              We serve North Idaho and the surrounding Inland Northwest. If you're envisioning a home in mountain or lake country, let's begin a conversation.
            </p>
          </div>
        </div>
        
        <div style={{ marginTop: '3rem', textAlign: 'center' }}>
          <Button href="/contact" variant="primary">
            Get in Touch
          </Button>
        </div>
      </Section>
    </>
  )
}
