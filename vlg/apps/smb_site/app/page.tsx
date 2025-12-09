import Hero from './components/Hero'
import TrustBar from './components/TrustBar'
import Section from './components/Section'
import Button from './components/Button'
import ProcessSteps from './components/ProcessSteps'
import styles from './page.module.css'

export default function Home() {
  return (
    <>
      <Hero />
      
      <TrustBar />
      
      <Section
        title="Mountain-Modern, Inside and Out."
        subtitle="We build homes that feel at home in the mountains: clean lines, warm materials, big glass, and thoughtful details. Whether it's a full custom home or a Sugar Mountain–designed spec, every project balances design, durability, and buildability."
        variant="default"
      >
        <div className={styles.serviceGrid}>
          <div className={styles.serviceCard}>
            <h3 className={styles.serviceTitle}>Custom & Semi-Custom Homes</h3>
            <p className={styles.serviceDescription}>
              We work with you from concept through completion—floor plans, specs, finishes, and construction. You get a single team managing the full build.
            </p>
          </div>
          <div className={styles.serviceCard}>
            <h3 className={styles.serviceTitle}>Spec & Investment Homes</h3>
            <p className={styles.serviceDescription}>
              Sugar Mountain Builders also develops its own spec homes and joint-venture projects. These use proven floor plans, tight budgets, and reliable schedules to create value for investors and future owners.
            </p>
          </div>
        </div>
        <div className={styles.ctaWrapper}>
          <Button href="/our-homes" variant="primary">
            See Our Work
          </Button>
        </div>
      </Section>
      
      <Section
        title="Modular Homes, Finished Like Custom."
        subtitle="We partner with Stax to install modern modular homes on permanent foundations. You get factory-built efficiency plus on-site craftsmanship."
        variant="dark"
      >
        <ul className={styles.modularList}>
          <li>Foundation, utilities, and site work</li>
          <li>Crane/set coordination</li>
          <li>Exterior decks, steps, and porches</li>
          <li>Interior finish, trim, and built-ins</li>
          <li>Permitting and inspections</li>
        </ul>
        <div className={styles.ctaWrapper}>
          <Button href="/modular-installs" variant="secondary">
            Learn About Modular Installs
          </Button>
        </div>
      </Section>
      
      <Section
        title="Make the Home You Have Feel Like the One You Want."
        subtitle="Kitchens, additions, whole-house refreshes, and 'this place needs to actually work for us now' remodels. We bring the same planning and schedule discipline to remodels that we do to new construction."
        variant="default"
      >
        <div className={styles.ctaWrapper}>
          <Button href="/remodels-additions" variant="primary">
            See Remodel Services
          </Button>
        </div>
      </Section>
      
      <Section
        title="A Straightforward, Five-Phase Process."
        variant="light"
      >
        <ProcessSteps />
        <div className={styles.ctaWrapper}>
          <Button href="/process" variant="primary">
            Learn More About Our Process
          </Button>
        </div>
      </Section>
      
      <Section
        title="Who We Are."
        subtitle="Sugar Mountain Builders is a mountain-modern builder based in the Inland Northwest. We combine field experience, cost control, and a design-forward mindset to deliver homes that feel as good to live in as they look in photos."
        variant="default"
      >
        <ul className={styles.valuesList}>
          <li>Tell the truth, even when it's inconvenient.</li>
          <li>Protect the schedule and the budget.</li>
          <li>Design for how people actually live.</li>
          <li>Build like we have to come back every winter.</li>
        </ul>
        <div className={styles.ctaWrapper}>
          <Button href="/about" variant="primary">
            Learn More About Us
          </Button>
        </div>
      </Section>
      
      <Section
        title="Ready to Talk About Your Project?"
        subtitle="Whether you're exploring modular, thinking about a spec home, or starting a full custom build, we're happy to look at your site and help you understand realistic paths forward."
        variant="accent"
      >
        <div className={styles.ctaGroup}>
          <Button href="/contact" variant="primary">
            Schedule a Call
          </Button>
          <Button href="/contact" variant="secondary">
            Send Us Your Plans
          </Button>
        </div>
      </Section>
    </>
  )
}
