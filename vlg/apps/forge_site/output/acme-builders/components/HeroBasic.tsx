import React from 'react';

interface HeroBasicProps {
  headline: string;
  subheadline: string;
  primaryCTA: {
    label: string;
    href: string;
  };
  heroImage?: string;
  secondaryCTA?: {
    label: string;
    href: string;
  };
}

export default function HeroBasic({
  headline,
  subheadline,
  primaryCTA,
  heroImage,
  secondaryCTA,
}: HeroBasicProps) {
  // Fallback copy in Karl + Hemingway style
  const displayHeadline = headline || 'Your business. Clearly presented.';
  const displaySubheadline = subheadline || 'We build clean websites that work.';
  const displayPrimaryLabel = primaryCTA?.label || 'Get started';
  const displayPrimaryHref = primaryCTA?.href || '#contact';

  return (
    <section className="bg-background py-20 px-4">
      <div className="max-w-4xl mx-auto text-center">
        <h1 className="text-4xl md:text-5xl font-bold text-text mb-6">
          {displayHeadline}
        </h1>
        <p className="text-xl text-text/80 mb-8 max-w-2xl mx-auto">
          {displaySubheadline}
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <a
            href={displayPrimaryHref}
            className="bg-primary text-white px-8 py-3 rounded-lg font-medium hover:opacity-90 transition inline-block"
          >
            {displayPrimaryLabel}
          </a>
          {secondaryCTA && (
            <a
              href={secondaryCTA.href}
              className="bg-mutedSurface text-text px-8 py-3 rounded-lg font-medium hover:opacity-90 transition inline-block"
            >
              {secondaryCTA.label}
            </a>
          )}
        </div>
        {heroImage && (
          <div className="mt-12">
            <img
              src={heroImage}
              alt=""
              className="w-full max-w-3xl mx-auto rounded-lg"
            />
          </div>
        )}
      </div>
    </section>
  );
}

