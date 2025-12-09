import React from 'react';

interface Service {
  name: string;
  shortDescription?: string;
  flagship?: boolean;
}

interface ServicesGridProps {
  services: Service[];
  serviceIcons?: string[];
  serviceImages?: string[];
}

export default function ServicesGrid({
  services,
  serviceIcons,
  serviceImages,
}: ServicesGridProps) {
  if (!services || services.length === 0) {
    return null;
  }

  return (
    <section className="py-16 px-4 bg-background">
      <div className="max-w-6xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {services.map((service, index) => (
            <div
              key={index}
              className="bg-white p-6 rounded-lg border border-mutedSurface hover:shadow-lg transition"
            >
              {serviceImages && serviceImages[index] && (
                <img
                  src={serviceImages[index]}
                  alt={service.name}
                  className="w-full h-48 object-cover rounded mb-4"
                />
              )}
              {serviceIcons && serviceIcons[index] && !serviceImages?.[index] && (
                <div className="text-4xl mb-4">{serviceIcons[index]}</div>
              )}
              <h3 className="text-xl font-semibold text-text mb-2">
                {service.name}
                {service.flagship && (
                  <span className="ml-2 text-sm text-primary">Featured</span>
                )}
              </h3>
              {service.shortDescription && (
                <p className="text-text/80">{service.shortDescription}</p>
              )}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

