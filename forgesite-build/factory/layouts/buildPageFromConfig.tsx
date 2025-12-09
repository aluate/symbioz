import React from 'react';
import { SiteConfig } from '@/factory/schemas/intake';
import { Hero } from '@/factory/modules/Hero';
import { ServicesGrid } from '@/factory/modules/ServicesGrid';
import { ProjectGallery } from '@/factory/modules/ProjectGallery';
import { TestimonialStrip } from '@/factory/modules/TestimonialStrip';
import { ProcessSteps } from '@/factory/modules/ProcessSteps';
import { LeadCaptureSection } from '@/factory/modules/LeadCaptureSection';
import { ContactBlock } from '@/factory/modules/ContactBlock';
import { FAQSection } from '@/factory/modules/FAQSection';
import { TrustBar } from '@/factory/modules/TrustBar';
import { SplitFeature } from '@/factory/modules/SplitFeature';

const MODULE_MAP: Record<string, React.ComponentType<any>> = {
  'hero': Hero,
  'services-grid': ServicesGrid,
  'project-gallery': ProjectGallery,
  'testimonial-strip': TestimonialStrip,
  'process-steps': ProcessSteps,
  'lead-capture': LeadCaptureSection,
  'contact-block': ContactBlock,
  'faq-section': FAQSection,
  'trust-bar': TrustBar,
  'split-feature': SplitFeature,
};

export function buildPageFromConfig(config: SiteConfig, pageRoute: string) {
  const page = config.pages.find(p => p.route === pageRoute);
  if (!page) return null;

  return page.modules.map((module, idx) => {
    const Component = MODULE_MAP[module.type];
    if (!Component) {
      console.warn(`Unknown module type: ${module.type}`);
      return null;
    }
    return <Component key={idx} {...module.props} brandColors={config.business.brandColors} />;
  });
}
