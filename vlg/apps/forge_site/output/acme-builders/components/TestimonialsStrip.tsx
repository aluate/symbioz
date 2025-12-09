import React from 'react';

interface Testimonial {
  quote: string;
  name?: string;
  role?: string;
  location?: string;
}

interface TestimonialsStripProps {
  testimonials: Testimonial[];
  testimonialImages?: string[];
  testimonialNames?: string[];
  testimonialRoles?: string[];
}

export default function TestimonialsStrip({
  testimonials,
  testimonialImages,
  testimonialNames,
  testimonialRoles,
}: TestimonialsStripProps) {
  if (!testimonials || testimonials.length === 0) {
    return null;
  }

  return (
    <section className="py-16 px-4 bg-mutedSurface/30">
      <div className="max-w-6xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {testimonials.map((testimonial, index) => {
            const name = testimonial.name || 
              (testimonialNames && testimonialNames[index]) ||
              'Client';
            const role = testimonial.role || 
              (testimonialRoles && testimonialRoles[index]) ||
              '';
            const image = testimonialImages && testimonialImages[index];
            const quote = testimonial.quote || 
              'They delivered quality work on time.';

            return (
              <div
                key={index}
                className="bg-white p-6 rounded-lg border border-mutedSurface"
              >
                <p className="text-text mb-4 italic">"{quote}"</p>
                <div className="flex items-center gap-4">
                  {image && (
                    <img
                      src={image}
                      alt={name}
                      className="w-12 h-12 rounded-full object-cover"
                    />
                  )}
                  <div>
                    <p className="font-semibold text-text">{name}</p>
                    {role && (
                      <p className="text-sm text-text/60">{role}</p>
                    )}
                    {testimonial.location && (
                      <p className="text-sm text-text/60">{testimonial.location}</p>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}

