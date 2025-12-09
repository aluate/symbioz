import React from 'react';

interface Project {
  title: string;
  location?: string;
  type?: string;
  images?: string[];
  description?: string;
}

interface ProjectGalleryGridProps {
  projects: Project[];
  projectDescriptions?: string[];
  projectLinks?: string[];
}

export default function ProjectGalleryGrid({
  projects,
  projectDescriptions,
  projectLinks,
}: ProjectGalleryGridProps) {
  if (!projects || projects.length === 0) {
    return null;
  }

  return (
    <section className="py-16 px-4 bg-white">
      <div className="max-w-6xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {projects.map((project, index) => {
            const firstImage = project.images && project.images.length > 0 
              ? project.images[0] 
              : null;
            const description = project.description || 
              (projectDescriptions && projectDescriptions[index]) ||
              'Quality work delivered on time.';
            const link = projectLinks && projectLinks[index];

            const content = (
              <div className="bg-background rounded-lg overflow-hidden hover:shadow-lg transition">
                {firstImage && (
                  <img
                    src={firstImage}
                    alt={project.title}
                    className="w-full h-64 object-cover"
                  />
                )}
                <div className="p-6">
                  <h3 className="text-xl font-semibold text-text mb-2">
                    {project.title}
                  </h3>
                  {project.location && (
                    <p className="text-sm text-text/60 mb-2">{project.location}</p>
                  )}
                  {project.type && (
                    <p className="text-sm text-primary mb-3">{project.type}</p>
                  )}
                  <p className="text-text/80">{description}</p>
                </div>
              </div>
            );

            if (link) {
              return (
                <a key={index} href={link} className="block">
                  {content}
                </a>
              );
            }

            return <div key={index}>{content}</div>;
          })}
        </div>
      </div>
    </section>
  );
}

