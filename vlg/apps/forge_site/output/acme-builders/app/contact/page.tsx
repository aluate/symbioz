import React from 'react';
import HeroBasic from '@/components/HeroBasic';
import ContactFormSimple from '@/components/ContactFormSimple';

export default function Contact() {
  return (
    <main>
      <HeroBasic headline="Acme Builders — Quality custom home construction and remodels in the Pacific Northwest" subheadline="Quality custom home construction and remodels in the Pacific Northwest" primaryCTA={{"label":"Get in touch","href":"/contact"}} />
      <ContactFormSimple contact={{"phone":"503-555-0123","email":"info@acmebuilders.com","address":"123 Construction Way, Portland, OR 97201","preferredContactMethod":"all","hours":"Monday-Friday: 8am-5pm"}} />
    </main>
  );
}
