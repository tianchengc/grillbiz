export const BIO_CONFIG = {
  profile: {
    name: "Acme Corp",
    initials: "AC",
    avatarUrl: "/avatar.png",
    tagline: "Your Mindful Tagline Here",
    location: "City, Country",
    company: "Acme Corp",
    companyUrl: "https://example.com",
  },
  social: [
    {
      name: "Instagram",
      url: "https://instagram.com",
      icon: "instagram"
    },
    {
      name: "LinkedIn",
      url: "https://linkedin.com",
      icon: "linkedin"
    },
    {
      name: "Email",
      url: "mailto:info@example.com",
      icon: "mail"
    }
  ],
  links: [
    {
      title: "🍵 Link 1 (e.g. Booking Link)",
      url: "https://example.com/book"
    },
    {
      title: "✉️ Link 2 (e.g. Contact Form)",
      url: "#contact"
    }
  ],
  projects: [] as { title: string; description: string; url: string; imageUrl: string; badge?: string }[],
  theme: {
    primary: "#4a7c59",
    accent: "#a8c5b0",
    background: "#fafaf8",
    text: "#1c1c1c",
    font: "Cormorant Garamond",
    fontSans: "Inter",
  },
} as const;

export type BioConfig = typeof BIO_CONFIG;
