import { BIO_CONFIG } from "@/data/site-config";
import { BlurFade } from "@/components/magicui/blur-fade";
import Link from "next/link";

export function BioLinks() {
  return (
    <section className="flex w-full flex-col items-center gap-3 px-4 py-4">
      {BIO_CONFIG.links.map((link, i) => {
        const isExternal = link.url.startsWith("http");
        return (
          <BlurFade key={link.url} delay={0.3 + i * 0.07}>
            <Link
              href={link.url}
              target={isExternal ? "_blank" : undefined}
              rel={isExternal ? "noopener noreferrer" : undefined}
              className="group flex w-full max-w-sm items-center justify-center rounded-xl border border-primary/20 bg-white px-5 py-3.5 text-sm font-medium text-gray-800 shadow-sm transition-all duration-200 hover:border-primary/50 hover:bg-primary/5 hover:shadow-md active:scale-[0.98]"
            >
              <span className="truncate">{link.title}</span>
              <svg
                className="ml-2 h-3.5 w-3.5 flex-shrink-0 text-gray-400 transition-transform duration-200 group-hover:translate-x-0.5 group-hover:text-primary"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                strokeWidth={2}
              >
                <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7" />
              </svg>
            </Link>
          </BlurFade>
        );
      })}
    </section>
  );
}
