'use client';

interface Step {
  title: string;
  description: string;
  icon?: string;
}

interface ProcessStepsProps {
  steps: Step[];
  brandColors?: {
    primary?: string;
    secondary?: string;
  };
}

export function ProcessSteps({ steps, brandColors }: ProcessStepsProps) {
  const primaryColor = brandColors?.primary || 'bg-blue-600';

  return (
    <section className="py-16 px-4">
      <div className="max-w-6xl mx-auto">
        <h2 className="text-3xl font-bold text-center mb-12">How We Work</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {steps.map((step, idx) => (
            <div key={idx} className="text-center">
              <div className={`w-16 h-16 ${primaryColor} rounded-full flex items-center justify-center mx-auto mb-4 text-white text-2xl font-bold`}>
                {step.icon || (idx + 1)}
              </div>
              <h3 className="text-xl font-semibold mb-2">{step.title}</h3>
              <p className="text-gray-600">{step.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
