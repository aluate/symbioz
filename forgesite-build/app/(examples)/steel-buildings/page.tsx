import { buildPageFromConfig } from '@/factory/layouts/buildPageFromConfig';
import steelIntake from '@/intake/examples/steel-buildings.json';
import { SiteConfig } from '@/factory/schemas/intake';

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
              subheadline: `Durable steel structures across ${intake.serviceArea}`,
              primaryCta: {
                text: 'Get a Quote',
                href: '#contact'
              },
              secondaryCta: {
                text: 'Learn More',
                href: '#services'
              }
            }
          },
          {
            type: 'services-grid',
            props: {
              services: intake.services.map((s: string) => ({ name: s })),
              columns: 2
            }
          },
          {
            type: 'testimonial-strip',
            props: {
              testimonials: intake.testimonials || []
            }
          },
          {
            type: 'lead-capture',
            props: {
              title: 'Request a Quote'
            }
          }
        ]
      }
    ],
    seo: {
      title: `${intake.businessName} - Steel Buildings in ${intake.serviceArea}`,
      description: `Commercial and agricultural steel structures. ${intake.services.join(', ')}.`
    }
  };
}

export default function SteelBuildingsExamplePage() {
  const config = generateSiteConfig(steelIntake);
  const modules = buildPageFromConfig(config, '/');

  return (
    <div>
      {modules}
    </div>
  );
}
