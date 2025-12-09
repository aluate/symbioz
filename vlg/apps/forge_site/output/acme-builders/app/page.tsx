import React from 'react';
import HeroBasic from '@/components/HeroBasic';
import TestimonialsStrip from '@/components/TestimonialsStrip';

export default function Home() {
  return (
    <main>
      <HeroBasic headline="Acme Builders — Quality custom home construction and remodels in the Pacific Northwest" subheadline="Quality custom home construction and remodels in the Pacific Northwest" primaryCTA={{"label":"Get in touch","href":"/contact"}} />
      <TestimonialsStrip testimonials={[{"quote":"Acme Builders delivered exactly what they promised. Quality work, on time, on budget.","name":"Sarah Johnson","role":"Homeowner","location":"Portland, OR"},{"quote":"Professional, reliable, and honest. Would hire again in a heartbeat.","name":"Mike Chen","role":"Homeowner","location":"Beaverton, OR"}]} />
    </main>
  );
}
