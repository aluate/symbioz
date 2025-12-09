/**
 * Floor Plans Page
 * 
 * Interactive floor plan builder for Sugar Mountain Builders.
 * Allows clients to explore default floor plans and customize configurations.
 */

import Section from '../components/Section'
import Button from '../components/Button'
import FloorPlanBuilder from '../components/FloorPlanBuilder/FloorPlanBuilder'
import styles from './page.module.css'

export default function FloorPlansPage() {
  return (
    <>
      <Section variant="dark" className={styles.hero}>
        <div className={styles.heroContent}>
          <h1 className={styles.heroTitle}>Explore Design Possibilities</h1>
          <p className={styles.heroSubtitle}>
            Our sophisticated floor plan builder lets you see how precision-built modules 
            come together to create your ideal mountain home. Start with one of our proven 
            layouts, or begin with a curated starting point and explore variations.
          </p>
          <p className={styles.heroNote}>
            This concept exploration tool gives you instant feedback on spatial flow and 
            module configuration. Final plans, engineering, and coordination are handled 
            by our team—ensuring every detail meets our standards for precision and craftsmanship.
          </p>
        </div>
      </Section>

      <Section variant="default">
        <div className={styles.defaultPlans}>
          <h2 className={styles.sectionTitle}>Start with a Proven Layout</h2>
          <p className={styles.sectionIntro}>
            Each of our default floor plans represents a refined starting point—optimized 
            for modular construction and designed for mountain living.
          </p>

          <div className={styles.planGrid}>
            {/* Sugarline 65 */}
            <div className={styles.planCard}>
              <div className={styles.planHeader}>
                <h3 className={styles.planName}>Sugarline 65</h3>
                <p className={styles.planSize}>1,040 sq ft • Single Module</p>
              </div>
              <div className={styles.planPreview}>
                <div className={styles.planPlaceholder}>
                  16' × 65' Floor Plan Preview
                </div>
              </div>
              <p className={styles.planDescription}>
                A single-module foundation perfect for starter homes, guest houses, 
                or ADUs. Efficient, elegant, and built with the same precision as 
                our larger configurations.
              </p>
              <div className={styles.planDetails}>
                <div className={styles.detailItem}>
                  <span className={styles.detailLabel}>Modules:</span>
                  <span className={styles.detailValue}>1</span>
                </div>
                <div className={styles.detailItem}>
                  <span className={styles.detailLabel}>Estimated Base:</span>
                  <span className={styles.detailValue}>$200,000</span>
                </div>
              </div>
              <Button href="#builder" variant="outline" className={styles.planButton}>
                Explore This Layout
              </Button>
            </div>

            {/* Twinline 130 */}
            <div className={styles.planCard}>
              <div className={styles.planHeader}>
                <h3 className={styles.planName}>Twinline 130</h3>
                <p className={styles.planSize}>2,080 sq ft • Two Modules</p>
              </div>
              <div className={styles.planPreview}>
                <div className={styles.planPlaceholder}>
                  Two 16' × 65' Modules, Offset Configuration
                </div>
              </div>
              <p className={styles.planDescription}>
                Two modules in an offset configuration, creating a split-floor-plan 
                layout. Bedrooms on opposite ends, great room connecting the space— 
                ideal for families seeking privacy and flow.
              </p>
              <div className={styles.planDetails}>
                <div className={styles.detailItem}>
                  <span className={styles.detailLabel}>Modules:</span>
                  <span className={styles.detailValue}>2</span>
                </div>
                <div className={styles.detailItem}>
                  <span className={styles.detailLabel}>Estimated Base:</span>
                  <span className={styles.detailValue}>$400,000</span>
                </div>
              </div>
              <Button href="#builder" variant="outline" className={styles.planButton}>
                Explore This Layout
              </Button>
            </div>

            {/* Summit Stack */}
            <div className={styles.planCard}>
              <div className={styles.planHeader}>
                <h3 className={styles.planName}>Summit Stack</h3>
                <p className={styles.planSize}>4,160 sq ft • Four Modules</p>
              </div>
              <div className={styles.planPreview}>
                <div className={styles.planPlaceholder}>
                  Four Modules, Two-Story Configuration
                </div>
              </div>
              <p className={styles.planDescription}>
                Four modules in a two-story configuration, creating a spacious 
                mountain estate home. Staircase modules connect levels, allowing 
                for multiple configurations within proven parameters.
              </p>
              <div className={styles.planDetails}>
                <div className={styles.detailItem}>
                  <span className={styles.detailLabel}>Modules:</span>
                  <span className={styles.detailValue}>4</span>
                </div>
                <div className={styles.detailItem}>
                  <span className={styles.detailLabel}>Estimated Base:</span>
                  <span className={styles.detailValue}>$800,000</span>
                </div>
              </div>
              <Button href="#builder" variant="outline" className={styles.planButton}>
                Explore This Layout
              </Button>
            </div>
          </div>
        </div>
      </Section>

      <Section variant="light" id="builder">
        <div className={styles.builderSection}>
          <h2 className={styles.sectionTitle}>Interactive Floor Plan Builder</h2>
          <p className={styles.sectionIntro}>
            A sophisticated design tool that lets you explore variations, 
            understand spatial relationships, and see real-time pricing. Our modular 
            room system allows you to understand how precision-built components come 
            together to create your ideal configuration.
          </p>
          
          <div className={styles.builderContainer}>
            <FloorPlanBuilder />
          </div>
        </div>
      </Section>

      <Section variant="dark">
        <div className={styles.whyModular}>
          <h2 className={styles.sectionTitle}>Why Precision Modular Construction</h2>
          <p className={styles.sectionIntro}>
            Modular construction isn't about compromise—it's about a more controlled 
            process that delivers superior results. Factory-built modules arrive on 
            your site weather-tight, with precision that's difficult to achieve in 
            traditional stick-built construction.
          </p>
          
          <div className={styles.benefitsGrid}>
            <div className={styles.benefitItem}>
              <h3 className={styles.benefitTitle}>Predictable Timeline</h3>
              <p className={styles.benefitDescription}>
                Factory-controlled conditions eliminate weather delays. Your home 
                arrives on schedule, ready for finish work.
              </p>
            </div>
            <div className={styles.benefitItem}>
              <h3 className={styles.benefitTitle}>Superior Quality</h3>
              <p className={styles.benefitDescription}>
                Precision engineering and controlled construction environments result 
                in tighter tolerances and better performance.
              </p>
            </div>
            <div className={styles.benefitItem}>
              <h3 className={styles.benefitTitle}>Design Flexibility</h3>
              <p className={styles.benefitDescription}>
                Our modular system allows for sophisticated configurations while 
                maintaining the efficiency of factory production.
              </p>
            </div>
            <div className={styles.benefitItem}>
              <h3 className={styles.benefitTitle}>Mountain-Tested</h3>
              <p className={styles.benefitDescription}>
                Every module is engineered for mountain conditions—snow loads, 
                temperature extremes, and the realities of alpine living.
              </p>
            </div>
          </div>
        </div>
      </Section>

      <Section variant="default">
        <div className={styles.ctaSection}>
          <h2 className={styles.ctaTitle}>Ready to Explore Your Options?</h2>
          <p className={styles.ctaText}>
            Whether you're interested in one of our default floor plans or have a 
            specific vision in mind, we're here to help you understand what's 
            possible with precision modular construction.
          </p>
          <div className={styles.ctaButtons}>
            <Button href="/contact" variant="primary">
              Schedule a Consultation
            </Button>
            <Button href="/our-homes" variant="outline">
              View Our Work
            </Button>
          </div>
        </div>
      </Section>
    </>
  )
}

