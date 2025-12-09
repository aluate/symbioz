'use client';

interface Project {
  title: string;
  image: string;
  description?: string;
  category?: string;
}

interface ProjectGalleryProps {
  projects: Project[];
  columns?: number;
}

export function ProjectGallery({ projects, columns = 3 }: ProjectGalleryProps) {
  const gridCols = columns === 2 ? 'md:grid-cols-2' : columns === 4 ? 'md:grid-cols-4' : 'md:grid-cols-3';

  return (
    <section className="py-16 px-4">
      <div className="max-w-7xl mx-auto">
        <h2 className="text-3xl font-bold text-center mb-12">Our Projects</h2>
        <div className={`grid grid-cols-1 ${gridCols} gap-6`}>
          {projects.map((project, idx) => (
            <div key={idx} className="group cursor-pointer">
              <div className="relative overflow-hidden rounded-lg aspect-[4/3] mb-4">
                <img 
                  src={project.image} 
                  alt={project.title}
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                />
                <div className="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-colors"></div>
              </div>
              <h3 className="text-xl font-semibold mb-1">{project.title}</h3>
              {project.category && (
                <p className="text-sm text-gray-500 mb-2">{project.category}</p>
              )}
              {project.description && (
                <p className="text-gray-600">{project.description}</p>
              )}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
