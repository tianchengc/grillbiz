import { BIO_CONFIG } from "@/data/site-config";
import { BlurFade } from "@/components/magicui/blur-fade";
import { BorderBeam } from "@/components/magicui/border-beam";
import Image from "next/image";

export function BioHero() {
  const { profile } = BIO_CONFIG;
  return (
    <section className="flex flex-col items-center gap-4 pt-16 pb-8 text-center">
      <BlurFade delay={0.05}>
        <div className="relative inline-block">
          <div className="relative h-28 w-28 overflow-hidden rounded-full border-2 border-white shadow-xl ring-2 ring-primary/20">
            <Image
              src={profile.avatarUrl}
              alt={profile.name}
              fill
              className="object-cover"
              priority
            />
            <BorderBeam
              colorFrom={BIO_CONFIG.theme.primary}
              colorTo={BIO_CONFIG.theme.accent}
              size={80}
              duration={8}
            />
          </div>
        </div>
      </BlurFade>

      <BlurFade delay={0.1}>
        <div className="space-y-1">
          <h1 className="text-2xl font-bold tracking-tight text-gray-900">
            {profile.name}
          </h1>
          <p className="text-sm font-medium text-primary">{profile.company}</p>
          <p className="text-xs text-gray-500">{profile.location}</p>
        </div>
      </BlurFade>

      <BlurFade delay={0.15}>
        <p className="max-w-xs text-sm leading-relaxed text-gray-600">
          {profile.tagline}
        </p>
      </BlurFade>
    </section>
  );
}
