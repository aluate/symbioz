'use client';

interface Badge {
  label: string;
  icon?: string;
}

interface TrustBarProps {
  badges: Badge[];
  layout?: 'horizontal' | 'grid';
}

export function TrustBar({ badges, layout = 'horizontal' }: TrustBarProps) {
  const isGrid = layout === 'grid';

  return (
    <section className="py-12 px-4 bg-white border-y">
      <div className="max-w-7xl mx-auto">
        <div className={`${isGrid ? 'grid grid-cols-2 md:grid-cols-4 gap-6' : 'flex flex-wrap justify-center items-center gap-8'}`}>
          {badges.map((badge, idx) => (
            <div key={idx} className="text-center">
              {badge.icon && (
                <div className="text-3xl mb-2">{badge.icon}</div>
              )}
              <p className="text-sm font-medium text-gray-700">{badge.label}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
