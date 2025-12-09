import { buildPageFromConfig } from '@/factory/layouts/buildPageFromConfig';
import cabinetIntake from '@/intake/examples/cabinet-shop.json';
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
              subheadline: `Custom cabinetry and millwork in ${intake.serviceArea}`,
              primaryCta: {
                text: 'Start Your Project',
                href: '#contact'
              }
            }
          },
          {
            type: 'services-grid',
            props: {
              services: intake.services.map((s: string) => ({ name: s })),
              columns: 3
            }
          },
          {
            type: 'testimonial-strip',
            props: {
              testimonials: intake.testimonials || [],
              layout: 'grid'
            }
          },
          {
            type: 'contact-block',
            props: {
              contact: intake.contact,
              layout: 'horizontal'
            }
          }
        ]
      }
    ],
    seo: {
      title: `${intake.businessName} - Custom Cabinetry in ${intake.serviceArea}`,
      description: `Premium custom cabinetry and millwork. ${intake.services.join(', ')}.`
    }
  };
}

export default function CabinetShopExamplePage() {
  const config = generateSiteConfig(cabinetIntake);
  const modules = buildPageFromConfig(config, '/');

  return (
    <div>
      {modules}
    </div>
  );
}
