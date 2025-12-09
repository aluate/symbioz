'use client';

interface Service {
  name: string;
  description?: string;
  icon?: string;
}

interface ServicesGridProps {
  services: Service[];
  columns?: number;
  brandColors?: {
    primary?: string;
    secondary?: string;
  };
}

export function ServicesGrid({ 
  services, 
  columns = 3,
  brandColors 
}: ServicesGridProps) {
  const gridCols = columns === 2 ? 'md:grid-cols-2' : columns === 4 ? 'md:grid-cols-4' : 'md:grid-cols-3';
  const primaryColor = brandColors?.primary || 'text-blue-600';

  return (
    <section className="py-16 px-4 bg-gray-50">
      <div className="max-w-7xl mx-auto">
        <h2 className="text-3xl font-bold text-center mb-12">Our Services</h2>
        <div className={`grid grid-cols-1 ${gridCols} gap-8`}>
          {services.map((service, idx) => (
            <div 
              key={idx}
              className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow"
            >
              {service.icon && (
                <div className={`text-4xl mb-4 ${primaryColor}`}>
                  {service.icon}
                </div>
              )}
              <h3 className="text-xl font-semibold mb-2">{service.name}</h3>
              {service.description && (
                <p className="text-gray-600">{service.description}</p>
              )}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
