import { STARTUP_CONFIG } from "@/data/site-config";
import { BentoGrid, BentoCard } from "@/components/magicui/bento-grid";
import { Coffee, Users, Leaf, Sparkles, HelpCircle } from "lucide-react";

const ICON_MAP: Record<string, React.ComponentType<{ className?: string }>> = {
  coffee: Coffee,
  users: Users,
  leaf: Leaf,
  sparkles: Sparkles,
};

export function HomeFeatures() {
  const { bentoFeatures } = STARTUP_CONFIG;
  return (
    <section className="mx-auto max-w-5xl px-6 py-16 md:py-24">
      <div className="text-center">
        <h2 className="font-serif text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
          Core Solutions
        </h2>
        <p className="mx-auto mt-4 max-w-2xl text-sm text-gray-500">
          How we solve your daily stress and tea sourcing challenges.
        </p>
      </div>

      <BentoGrid className="mt-12">
        {bentoFeatures.map((feature, i) => {
          const IconComponent = ICON_MAP[feature.icon.toLowerCase()] ?? HelpCircle;
          return (
            <BentoCard
              key={feature.title}
              name={feature.title}
              description={feature.description}
              Icon={IconComponent}
              className={feature.className}
              href={STARTUP_CONFIG.hero.primaryCta.href}
              cta="Book Now"
            />
          );
        })}
      </BentoGrid>
    </section>
  );
}
