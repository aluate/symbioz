'use client';

import { Button } from '@/components/ui/button';

interface HeroProps {
  headline: string;
  subheadline: string;
  primaryCta: {
    text: string;
    href: string;
  };
  secondaryCta?: {
    text: string;
    href: string;
  };
  backgroundImage?: string;
  brandColors?: {
    primary?: string;
    secondary?: string;
  };
}

export function Hero({
  headline,
  subheadline,
  primaryCta,
  secondaryCta,
  backgroundImage,
  brandColors
}: HeroProps) {
  const bgStyle = backgroundImage 
    ? { backgroundImage: `url(${backgroundImage})` }
    : {};
  const primaryColor = brandColors?.primary || 'bg-blue-600';
  const secondaryColor = brandColors?.secondary || 'bg-gray-600';

  return (
    <section 
      className="relative min-h-[600px] flex items-center justify-center bg-gray-900 text-white bg-cover bg-center"
      style={bgStyle}
    >
      <div className="absolute inset-0 bg-black/50"></div>
      <div className="relative z-10 max-w-4xl mx-auto px-4 text-center">
        <h1 className="text-5xl md:text-6xl font-bold mb-6">{headline}</h1>
        <p className="text-xl md:text-2xl mb-8 text-gray-200">{subheadline}</p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Button asChild className={`${primaryColor} hover:opacity-90`}>
            <a href={primaryCta.href}>{primaryCta.text}</a>
          </Button>
          {secondaryCta && (
            <Button asChild variant="outline" className="border-white text-white hover:bg-white/10">
              <a href={secondaryCta.href}>{secondaryCta.text}</a>
            </Button>
          )}
        </div>
      </div>
    </section>
  );
}
