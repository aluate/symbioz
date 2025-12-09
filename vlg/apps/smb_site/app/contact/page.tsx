import Section from '../components/Section'
import ContactForm from '../components/ContactForm'

export default function Contact() {
  return (
    <>
      <Section
        title="Let's Begin the Conversation."
        subtitle="Whether you're exploring modular construction, considering a spec home, or envisioning a full custom build, we're here to understand your vision and map a clear path forward."
        variant="default"
      >
        <div style={{ 
          display: 'grid',
          gridTemplateColumns: '1fr',
          gap: '3rem',
          marginTop: '2rem'
        }}>
          <div>
            <ContactForm />
          </div>
          
          <div style={{ 
            padding: '2rem',
            backgroundColor: 'var(--color-black)',
            color: 'white',
            borderRadius: '4px'
          }}>
            <h3 style={{ 
              fontFamily: 'var(--font-playfair)', 
              fontSize: '1.5rem', 
              fontWeight: 700, 
              marginBottom: '1.5rem',
              color: 'white'
            }}>
              Other Ways to Reach Us
            </h3>
            
            <div style={{ 
              fontFamily: 'var(--font-inter)',
              fontSize: '1rem',
              lineHeight: '1.8',
              color: 'rgba(255, 255, 255, 0.9)'
            }}>
              <p style={{ marginBottom: '1rem' }}>
                <strong>Email:</strong><br />
                <a href="mailto:info@sugarmountainbuilders.com" style={{ color: 'var(--color-tiffany-blue)' }}>
                  info@sugarmountainbuilders.com
                </a>
              </p>
              
              <p style={{ marginBottom: '1rem' }}>
                <strong>Phone:</strong><br />
                <a href="tel:+1-XXX-XXX-XXXX" style={{ color: 'var(--color-tiffany-blue)' }}>
                  (XXX) XXX-XXXX
                </a>
              </p>
              
              <p style={{ marginBottom: '1rem' }}>
                <strong>Service Area:</strong><br />
                North Idaho and surrounding Inland Northwest regions
              </p>
            </div>
          </div>
        </div>
      </Section>
    </>
  )
}
