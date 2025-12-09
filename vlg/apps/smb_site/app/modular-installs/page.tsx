import Section from '../components/Section'
import Button from '../components/Button'

export default function ModularInstalls() {
  return (
    <>
      <Section
        title="Modular Construction, Finished Like Custom."
        subtitle="We partner with Stax to install precision-built modular homes on permanent foundations. Factory-controlled quality meets on-site craftsmanship—delivering custom-level finishes with predictable timelines."
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
            Our modular installation service unites factory-controlled efficiency with the precision finish work expected from a custom builder. From site preparation through final walkthrough, we orchestrate every detail.
          </p>
          
          <h3 style={{ 
            fontFamily: 'var(--font-playfair)', 
            fontSize: '1.75rem', 
            fontWeight: 700, 
            marginTop: '2rem',
            marginBottom: '1rem',
            color: 'var(--color-black)'
          }}>
            What We Handle
          </h3>
          
          <ul style={{ 
            listStyle: 'none', 
            padding: 0,
            marginBottom: '2rem'
          }}>
            <li style={{ 
              padding: '0.75rem 0',
              paddingLeft: '2rem',
              position: 'relative'
            }}>
              <span style={{ 
                position: 'absolute',
                left: 0,
                color: 'var(--color-tiffany-blue)',
                fontWeight: 700
              }}>✓</span>
              <strong>Foundation, utilities, and site work</strong> – We prepare your site for the modular installation, ensuring proper foundation and utility connections.
            </li>
            <li style={{ 
              padding: '0.75rem 0',
              paddingLeft: '2rem',
              position: 'relative'
            }}>
              <span style={{ 
                position: 'absolute',
                left: 0,
                color: 'var(--color-tiffany-blue)',
                fontWeight: 700
              }}>✓</span>
              <strong>Crane/set coordination</strong> – We manage the logistics of bringing your modular units to the site and setting them in place.
            </li>
            <li style={{ 
              padding: '0.75rem 0',
              paddingLeft: '2rem',
              position: 'relative'
            }}>
              <span style={{ 
                position: 'absolute',
                left: 0,
                color: 'var(--color-tiffany-blue)',
                fontWeight: 700
              }}>✓</span>
              <strong>Exterior decks, steps, and porches</strong> – We add the finishing touches that make your modular home feel site-built.
            </li>
            <li style={{ 
              padding: '0.75rem 0',
              paddingLeft: '2rem',
              position: 'relative'
            }}>
              <span style={{ 
                position: 'absolute',
                left: 0,
                color: 'var(--color-tiffany-blue)',
                fontWeight: 700
              }}>✓</span>
              <strong>Interior finish, trim, and built-ins</strong> – Custom trim work and built-in features complete the home.
            </li>
            <li style={{ 
              padding: '0.75rem 0',
              paddingLeft: '2rem',
              position: 'relative'
            }}>
              <span style={{ 
                position: 'absolute',
                left: 0,
                color: 'var(--color-tiffany-blue)',
                fontWeight: 700
              }}>✓</span>
              <strong>Permitting and inspections</strong> – We handle all the paperwork and ensure everything meets code requirements.
            </li>
          </ul>
          
          <p style={{ 
            marginTop: '2rem',
            fontStyle: 'italic',
            color: 'var(--color-charcoal)'
          }}>
            Interested in learning more about modular homes? Visit <a href="#" style={{ color: 'var(--color-tiffany-blue)' }}>Stax</a> to see our modular product lineup.
          </p>
        </div>
        
        <div style={{ marginTop: '3rem', textAlign: 'center' }}>
          <Button href="/contact" variant="primary">
            Get Started with Modular
          </Button>
        </div>
      </Section>
    </>
  )
}
