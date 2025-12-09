import { buildPageFromConfig } from '@/factory/layouts/buildPageFromConfig';
import builderIntake from '@/intake/examples/builder.json';
import { SiteConfig } from '@/factory/schemas/intake';

// Generate site config from intake
function generateSiteConfig(intake: any): SiteConfig {
  return {
    business: intake,
    pages: [
      {
        route: '/',
        title: 'Home',
        modules: [
          {
            type: 'hero',
            props: {
              headline: intake.businessName,
              subheadline: `Professional ${intake.tradeType} services in ${intake.serviceArea}`,
              primaryCta: {
                text: 'Get a Quote',
                href: '#contact'
              },
              secondaryCta: {
                text: 'View Projects',
                href: '#projects'
              }
            }
          },
          {
            type: 'services-grid',
            props: {
              services: intake.services.map((s: string) => ({ name: s }))
            }
          },
          {
            type: 'testimonial-strip',
            props: {
              testimonials: intake.testimonials || []
            }
          },
          {
            type: 'contact-block',
            props: {
              contact: intake.contact
            }
          }
        ]
      }
    ],
    seo: {
      title: `${intake.businessName} - ${intake.tradeType} in ${intake.serviceArea}`,
      description: `Professional ${intake.tradeType} services. ${intake.services.join(', ')}.`
    }
  };
}

export default function BuilderExamplePage() {
  const config = generateSiteConfig(builderIntake);
  const modules = buildPageFromConfig(config, '/');

  return (
    <div>
      {modules}
    </div>
  );
}
