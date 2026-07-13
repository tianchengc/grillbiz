import { BioHero } from "@/components/bio-hero";
import { BioDock } from "@/components/bio-dock";
import { BioLinks } from "@/components/bio-links";
import { BioContact } from "@/components/bio-contact";
import { BIO_CONFIG } from "@/data/site-config";

export default function HomePage() {
  return (
    <main className="mx-auto flex min-h-screen max-w-md flex-col items-center pb-24 px-4 bg-background text-gray-900">
      {/* Hero: avatar + name + tagline */}
      <BioHero />

      {/* Social links dock */}
      <BioDock />

      {/* CTA action pills */}
      <BioLinks />

      {/* Contact Form */}
      <BioContact />

      {/* Footer */}
      <footer className="mt-auto pt-16 text-center text-xs text-gray-400">
        <a
          href={BIO_CONFIG.profile.companyUrl}
          target="_blank"
          rel="noopener noreferrer"
          className="hover:text-primary transition-colors font-medium font-serif"
        >
          {BIO_CONFIG.profile.company}
        </a>
        {" · "}
        <span>{BIO_CONFIG.profile.location}</span>
      </footer>
    </main>
  );
}
