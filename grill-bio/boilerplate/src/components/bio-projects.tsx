import { BIO_CONFIG } from "@/data/site-config";
import { BlurFade } from "@/components/magicui/blur-fade";
import { MagicCard } from "@/components/magicui/magic-card";
import Image from "next/image";
import Link from "next/link";

export function BioProjects() {
  if (!BIO_CONFIG.projects.length) return null;
  return (
    <section className="w-full px-4 py-6">
      <BlurFade delay={0.5}>
        <h2 className="mb-4 text-center text-xs font-semibold uppercase tracking-widest text-gray-400">
          Featured
        </h2>
      </BlurFade>
      <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
        {BIO_CONFIG.projects.map((project, i) => (
          <BlurFade key={project.url} delay={0.55 + i * 0.08}>
            <Link
              href={project.url}
              target="_blank"
              rel="noopener noreferrer"
              className="block"
            >
              <MagicCard
                className="flex flex-col overflow-hidden transition-shadow duration-200 hover:shadow-lg"
                gradientColor={`${BIO_CONFIG.theme.primary}18`}
              >
                {project.imageUrl && (
                  <div className="relative h-36 w-full overflow-hidden">
                    <Image
                      src={project.imageUrl}
                      alt={project.title}
                      fill
                      className="object-cover transition-transform duration-300 group-hover:scale-105"
                    />
                    {project.badge && (
                      <span className="absolute right-2 top-2 rounded-full bg-primary px-2 py-0.5 text-xs font-semibold text-white">
                        {project.badge}
                      </span>
                    )}
                  </div>
                )}
                <div className="p-3">
                  <p className="text-sm font-semibold text-gray-900">{project.title}</p>
                  <p className="mt-0.5 text-xs leading-relaxed text-gray-500">
                    {project.description}
                  </p>
                </div>
              </MagicCard>
            </Link>
          </BlurFade>
        ))}
      </div>
    </section>
  );
}
