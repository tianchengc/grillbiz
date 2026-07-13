import { STARTUP_CONFIG } from "@/data/site-config";
import { ShimmerButton } from "@/components/magicui/shimmer-button";
import Link from "next/link";

export function HomeHero() {
  const { hero } = STARTUP_CONFIG;
  return (
    <section className="relative flex flex-col items-center justify-center overflow-hidden px-6 pt-24 pb-16 text-center md:pt-32 md:pb-24">
      {/* Background Gradient */}
      <div className="absolute inset-0 -z-10 bg-[radial-gradient(45rem_50rem_at_50%_-10rem,var(--primary-glow),transparent)] opacity-40" />

      {/* Hero Badge */}
      {hero.badge && (
        <span className="inline-flex items-center rounded-full bg-primary/10 px-3 py-1 text-xs font-semibold text-primary ring-1 ring-inset ring-primary/20">
          {hero.badge}
        </span>
      )}

      {/* Hero Headline */}
      <h1 className="mx-auto mt-6 max-w-4xl font-serif text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl md:text-7xl leading-tight">
        {hero.heading}
      </h1>

      {/* Hero Subheading */}
      <p className="mx-auto mt-6 max-w-2xl text-lg leading-relaxed text-gray-600">
        {hero.subheading}
      </p>

      {/* Hero CTAs */}
      <div className="mt-10 flex flex-wrap items-center justify-center gap-4">
        <Link href={hero.primaryCta.href} target="_blank" rel="noopener noreferrer">
          <ShimmerButton background={STARTUP_CONFIG.theme.primary} className="shadow-lg">
            {hero.primaryCta.text}
          </ShimmerButton>
        </Link>
        {hero.secondaryCta && (
          <Link
            href={hero.secondaryCta.href}
            target="_blank"
            rel="noopener noreferrer"
            className="rounded-full border border-gray-300 bg-white/80 px-6 py-3 text-sm font-semibold text-gray-700 shadow-sm backdrop-blur-sm transition-all hover:bg-gray-50 active:scale-[0.98]"
          >
            {hero.secondaryCta.text}
          </Link>
        )}
      </div>
    </section>
  );
}
