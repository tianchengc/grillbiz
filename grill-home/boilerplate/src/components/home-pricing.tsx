import { STARTUP_CONFIG } from "@/data/site-config";
import { BorderBeam } from "@/components/magicui/border-beam";
import { ShimmerButton } from "@/components/magicui/shimmer-button";
import { Check } from "lucide-react";
import Link from "next/link";

export function HomePricing() {
  const { pricing } = STARTUP_CONFIG;
  if (!pricing || !pricing.length) return null;

  return (
    <section className="mx-auto max-w-5xl px-6 py-16 md:py-24 border-t border-gray-100">
      <div className="text-center">
        <h2 className="font-serif text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
          Simple, Transparent Pricing
        </h2>
        <p className="mx-auto mt-4 max-w-2xl text-sm text-gray-500">
          Book a direct-from-farm experience or corporate session tailored for your team.
        </p>
      </div>

      <div className="mt-12 grid grid-cols-1 gap-6 sm:grid-cols-2 max-w-3xl mx-auto">
        {pricing.map((plan) => (
          <div
            key={plan.plan}
            className={`relative flex flex-col justify-between rounded-2xl border p-8 shadow-sm transition-all duration-200 hover:shadow-md ${
              plan.highlighted
                ? "border-primary bg-primary/5 scale-105"
                : "border-gray-200 bg-white"
            }`}
          >
            {plan.highlighted && (
              <BorderBeam
                colorFrom={STARTUP_CONFIG.theme.primary}
                colorTo={STARTUP_CONFIG.theme.accent}
                size={200}
                duration={10}
              />
            )}

            <div>
              <h3 className="text-lg font-semibold text-gray-900">{plan.plan}</h3>
              <p className="mt-4 flex items-baseline">
                <span className="text-4xl font-bold tracking-tight text-gray-900">
                  {plan.price}
                </span>
                {plan.period && (
                  <span className="ml-1 text-sm font-semibold text-gray-500">
                    /{plan.period}
                  </span>
                )}
              </p>
              <ul className="mt-6 space-y-4">
                {plan.features.map((feature) => (
                  <li key={feature} className="flex items-start text-sm text-gray-600">
                    <Check className="mr-2 h-4 w-4 text-primary flex-shrink-0 mt-0.5" />
                    <span>{feature}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="mt-8">
              <Link href={plan.href} target="_blank" rel="noopener noreferrer">
                {plan.highlighted ? (
                  <ShimmerButton
                    background={STARTUP_CONFIG.theme.primary}
                    className="w-full shadow-lg"
                  >
                    {plan.cta}
                  </ShimmerButton>
                ) : (
                  <button className="w-full rounded-full border border-gray-300 bg-white px-4 py-2.5 text-sm font-semibold text-gray-700 shadow-sm transition hover:bg-gray-50 active:scale-[0.98]">
                    {plan.cta}
                  </button>
                )}
              </Link>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
