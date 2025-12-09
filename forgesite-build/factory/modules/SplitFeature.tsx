'use client';

import { Button } from '@/components/ui/button';

interface SplitFeatureProps {
  image: string;
  title: string;
  content: string;
  reverse?: boolean;
  cta?: {
    text: string;
    href: string;
  };
  brandColors?: {
    primary?: string;
    secondary?: string;
  };
}

export function SplitFeature({
  image,
  title,
  content,
  reverse = false,
  cta,
  brandColors
}: SplitFeatureProps) {
  const primaryColor = brandColors?.primary || 'bg-blue-600';
  const flexDirection = reverse ? 'md:flex-row-reverse' : 'md:flex-row';

  return (
    <section className="py-16 px-4">
      <div className="max-w-7xl mx-auto">
        <div className={`flex flex-col ${flexDirection} gap-8 items-center`}>
          <div className="flex-1">
            <img 
              src={image} 
              alt={title}
              className="w-full h-auto rounded-lg shadow-md"
            />
          </div>
          <div className="flex-1">
            <h2 className="text-3xl font-bold mb-4">{title}</h2>
            <p className="text-gray-600 mb-6 leading-relaxed">{content}</p>
            {cta && (
              <Button asChild className={`${primaryColor} hover:opacity-90`}>
                <a href={cta.href}>{cta.text}</a>
              </Button>
            )}
          </div>
        </div>
      </div>
    </section>
  );
}
