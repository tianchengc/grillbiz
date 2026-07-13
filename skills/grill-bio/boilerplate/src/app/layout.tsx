import type { Metadata } from "next";
import { Inter, Cormorant_Garamond } from "next/font/google";
import { BIO_CONFIG } from "@/data/site-config";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

const cormorant = Cormorant_Garamond({
  subsets: ["latin"],
  weight: ["300", "400", "500", "600", "700"],
  variable: "--font-cormorant",
  display: "swap",
});

export const metadata: Metadata = {
  title: `${BIO_CONFIG.profile.name} — ${BIO_CONFIG.profile.company}`,
  description: BIO_CONFIG.profile.tagline,
  openGraph: {
    title: `${BIO_CONFIG.profile.name} — ${BIO_CONFIG.profile.company}`,
    description: BIO_CONFIG.profile.tagline,
    type: "profile",
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${inter.variable} ${cormorant.variable}`}>
      <body className="bg-background font-sans text-gray-900 antialiased">
        {children}
      </body>
    </html>
  );
}
