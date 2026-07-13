import { STARTUP_CONFIG } from "@/data/site-config";
import { Marquee } from "@/components/magicui/marquee";

export function HomeMarquee() {
  const { socialProof } = STARTUP_CONFIG;
  if (!socialProof.companies.length) return null;
  return (
    <section className="border-y border-gray-100 bg-gray-50/50 py-6">
      <div className="mx-auto max-w-7xl px-6">
        <p className="text-center text-xs font-semibold uppercase tracking-widest text-gray-400">
          Recognized & Trusted By
        </p>
        <Marquee className="mt-4 [--duration:30s]" pauseOnHover>
          {socialProof.companies.map((company, i) => (
            <div
              key={`${company}-${i}`}
              className="mx-8 flex items-center justify-center font-serif text-lg font-medium text-gray-400"
            >
              {company}
            </div>
          ))}
        </Marquee>
      </div>
    </section>
  );
}
