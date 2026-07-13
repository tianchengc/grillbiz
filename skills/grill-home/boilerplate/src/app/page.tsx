"use client";
import React, { useState } from "react";
import Image from "next/image";
import { BlurFade } from "@/components/magicui/blur-fade";
import { BorderBeam } from "@/components/magicui/border-beam";
import { ShimmerButton } from "@/components/magicui/shimmer-button";
import { BentoGrid, BentoCard } from "@/components/magicui/bento-grid";
import { Marquee } from "@/components/magicui/marquee";
import { Coffee, Users, Leaf, Sparkles, Check, ChevronDown, Send, ArrowRight } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

// Inline Accordion Component for FAQs
function Accordion({ items }: { items: { question: string; answer: string }[] }) {
  const [activeIndex, setActiveIndex] = useState<number | null>(null);
  return (
    <div className="space-y-4 w-full max-w-3xl mx-auto text-left">
      {items.map((item, idx) => {
        const isOpen = activeIndex === idx;
        return (
          <div key={idx} className="border-b border-neutral-200 pb-4">
            <button
              onClick={() => setActiveIndex(isOpen ? null : idx)}
              className="flex w-full items-center justify-between py-4 text-left font-medium text-neutral-900 focus:outline-none"
            >
              <span className="text-base md:text-lg font-sans font-medium text-neutral-950">{item.question}</span>
              <ChevronDown className={`h-5 w-5 text-neutral-400 transition-transform duration-300 ${isOpen ? "rotate-180" : ""}`} />
            </button>
            <AnimatePresence initial={false}>
              {isOpen && (
                <motion.div
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: "auto", opacity: 1 }}
                  exit={{ height: 0, opacity: 0 }}
                  transition={{ duration: 0.3, ease: "easeInOut" }}
                  className="overflow-hidden"
                >
                  <p className="pr-12 text-sm md:text-base text-neutral-500 leading-relaxed pt-1 pb-3">{item.answer}</p>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        );
      })}
    </div>
  );
}

// Interactive Contact Form Component
function ContactForm() {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [name, setName] = useState("");
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || !message) return;
    setSubmitted(true);
  };

  return (
    <div className="w-full max-w-lg mx-auto bg-white/80 backdrop-blur-md border border-neutral-200 p-8 rounded-2xl shadow-sm relative text-left">
      <AnimatePresence mode="wait">
        {!submitted ? (
          <motion.form
            key="contact-form"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onSubmit={handleSubmit}
            className="space-y-4"
          >
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-neutral-500 mb-1">Name</label>
              <input
                type="text"
                required
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="w-full px-4 py-2 border border-neutral-200 rounded-lg text-sm bg-neutral-50/50 focus:outline-none focus:border-neutral-900 transition-colors"
                placeholder="Your Name"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-neutral-500 mb-1">Email</label>
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-4 py-2 border border-neutral-200 rounded-lg text-sm bg-neutral-50/50 focus:outline-none focus:border-neutral-900 transition-colors"
                placeholder="you@example.com"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-neutral-500 mb-1">Message</label>
              <textarea
                required
                rows={4}
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                className="w-full px-4 py-2 border border-neutral-200 rounded-lg text-sm bg-neutral-50/50 focus:outline-none focus:border-neutral-900 transition-colors resize-none"
                placeholder="How can we help you slow down?"
              />
            </div>
            <button
              type="submit"
              className="w-full mt-4 flex items-center justify-center gap-2 rounded-full bg-neutral-950 px-6 py-3 text-sm font-semibold text-white hover:bg-neutral-800 transition-all active:scale-[0.98] cursor-pointer"
            >
              <span>Send Message</span>
              <Send className="h-4 w-4" />
            </button>
          </motion.form>
        ) : (
          <motion.div
            key="success"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0 }}
            className="py-12 text-center flex flex-col items-center justify-center"
          >
            <div className="h-12 w-12 rounded-full bg-neutral-100 flex items-center justify-center mb-4 border border-neutral-200">
              <Check className="h-6 w-6 text-neutral-950" />
            </div>
            <h3 className="text-lg font-semibold text-neutral-950">Thank you, {name}!</h3>
            <p className="text-sm text-neutral-500 mt-2 max-w-xs">Your inquiry has been sent. We will get back to you at {email} within 24 hours.</p>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

export default function ChahavenHome() {
  const faqItems = [
    {
      question: "What is a Chinese tea ceremony (Gongfu Cha)?",
      answer: "Gongfu Cha translates to 'making tea with skill.' It is a traditional Chinese ritual focusing on brewing tea in small clay vessels with precise control over temperature and time. This slow extraction method allows you to experience the evolving aroma and flavor profile of each leaf steep."
    },
    {
      question: "Do I need prior experience to attend a ceremony?",
      answer: "Not at all. Our ceremonies are designed to be accessible and relaxing for beginners and tea connoisseurs alike. A seasoned tea master will guide you through the process, sharing the cultural history and meditation techniques."
    },
    {
      question: "How do I book a private group ceremony?",
      answer: "You can book individual seats through our Eventbrite page, or reach out directly via info@chahaven.ca to coordinate a private group or corporate team workshop at your convenience."
    },
    {
      question: "Where do you source your tea leaves?",
      answer: "All of our oolong leaves are organically grown and hand-harvested directly from our family's tea farm in Fujian, China, ensuring absolute single-origin quality and traceablity."
    }
  ];

  return (
    <main className="min-h-screen selection:bg-neutral-950/10 selection:text-neutral-950 overflow-x-hidden bg-neutral-50 text-neutral-900 font-sans">
      
      {/* Floating Header */}
      <header className="fixed top-4 left-0 right-0 z-50 mx-auto max-w-4xl px-4">
        <div className="flex h-14 items-center justify-between rounded-full border border-neutral-200/80 bg-white/70 px-6 backdrop-blur-md shadow-sm">
          <div className="flex items-center gap-2.5">
            <Image src="/logo.png" alt="Chahaven Logo" width={28} height={28} className="object-contain" />
            <span className="text-sm font-semibold tracking-wider uppercase text-neutral-950">Chahaven</span>
          </div>
          <nav className="flex items-center gap-6">
            <a href="#solutions" className="text-xs font-medium text-neutral-500 hover:text-neutral-950 transition-colors">Ceremonies</a>
            <a href="#faq" className="text-xs font-medium text-neutral-500 hover:text-neutral-950 transition-colors">FAQ</a>
            <a href="#contact" className="text-xs font-medium text-neutral-500 hover:text-neutral-950 transition-colors">Contact</a>
          </nav>
        </div>
      </header>

      {/* 1. Hero Section */}
      <section className="relative flex flex-col items-center justify-center px-6 pt-36 pb-24 text-center md:pt-48 md:pb-32 overflow-hidden border-b border-neutral-200/50 bg-white">
        {/* Architect Grid Backdrop */}
        <div className="absolute inset-0 -z-10 bg-[linear-gradient(to_right,rgba(0,0,0,0.015)_1px,transparent_1px),linear-gradient(to_bottom,rgba(0,0,0,0.015)_1px,transparent_1px)] bg-[size:24px_24px] opacity-60" />
        <div className="absolute inset-0 -z-10 bg-[radial-gradient(40rem_40rem_at_top,var(--primary-glow),transparent)] opacity-40" />

        <BlurFade delay={0.05}>
          <span className="inline-flex items-center rounded-full border border-neutral-200 bg-neutral-50 px-3.5 py-1 text-xs font-semibold tracking-wide text-neutral-950 shadow-sm">
            🇨🇳 Farm-Direct Premium Harvests
          </span>
        </BlurFade>

        <BlurFade delay={0.15}>
          <h1 className="mx-auto mt-8 max-w-4xl font-sans text-4xl font-extrabold tracking-tight text-neutral-950 sm:text-6xl md:text-7xl leading-none">
            Find Focus & Calm Through <span className="text-neutral-950 underline decoration-neutral-300 underline-offset-8">Drinkable Meditation</span>
          </h1>
        </BlurFade>

        <BlurFade delay={0.25}>
          <p className="mx-auto mt-8 max-w-2xl text-base md:text-lg leading-relaxed text-neutral-500">
            Escape the noise of Ottawa's tech grind. Experience private traditional Chinese tea ceremonies hosted by seasoned masters using organic single-origin leaves.
          </p>
        </BlurFade>

        <BlurFade delay={0.35}>
          <div className="mt-12 flex flex-wrap items-center justify-center gap-4">
            <a href="https://www.eventbrite.ca/o/chadynasty-tea-92288286313" target="_blank" rel="noopener noreferrer">
              <ShimmerButton background="rgba(15, 15, 15, 1)" className="shadow-md">
                Book a Ceremony
              </ShimmerButton>
            </a>
            <a
              href="mailto:info@chahaven.ca"
              className="rounded-full border border-neutral-250 bg-white px-6 py-3 text-sm font-semibold text-neutral-700 shadow-sm transition-all hover:bg-neutral-50 hover:text-neutral-950 active:scale-[0.98] flex items-center gap-2"
            >
              <span>Contact Us</span>
              <ArrowRight className="h-4 w-4" />
            </a>
          </div>
        </BlurFade>
      </section>

      {/* 2. Brand Quote Section */}
      <section className="bg-neutral-150 border-b border-neutral-200/50 py-16 text-center">
        <BlurFade delay={0.1}>
          <p className="mx-auto max-w-3xl text-xl md:text-2xl font-serif italic text-neutral-800 leading-relaxed px-6">
            "Slow down. Observe the steam. Breathe in the aroma of direct-sourced leaves. Connect offline."
          </p>
        </BlurFade>
      </section>

      {/* 3. Bento Solutions Grid */}
      <section id="solutions" className="mx-auto max-w-5xl px-6 py-20 md:py-28 text-center">
        <BlurFade delay={0.05}>
          <div>
            <h2 className="font-sans text-3xl font-extrabold tracking-tight text-neutral-950 sm:text-4xl">
              Mindful Tea Solutions
            </h2>
            <p className="mx-auto mt-4 max-w-2xl text-sm md:text-base text-neutral-500">
              Dissolve stress and discover premium cultural flavors through our ceremonies and harvests.
            </p>
          </div>
        </BlurFade>

        <div className="mt-16">
          <BentoGrid>
            <BentoCard
              name="Private Tea Ceremonies"
              description="Book an intimate 1-on-1 or small group session with a tea master to dissolve stress and find quiet focus."
              Icon={Coffee}
              className="col-span-3 lg:col-span-2 relative"
              href="https://www.eventbrite.ca/o/chadynasty-tea-92288286313"
              cta="Book Now"
            />
            <BentoCard
              name="Corporate Workshops"
              description="On-site wellness experiences bringing premium leaves, utensils, and relaxation rituals directly to your tech team's office."
              Icon={Users}
              className="col-span-3 lg:col-span-1"
              href="mailto:info@chahaven.ca"
              cta="Inquire"
            />
            <BentoCard
              name="Direct Sourced Oolong"
              description="Exclusive single-origin organic leaves harvested from our family tea farm in China, cutting out middlemen for unbeatable quality."
              Icon={Leaf}
              className="col-span-3 lg:col-span-1"
            />
            <BentoCard
              name="Starter Utensils"
              description="Everything you need to practice silent tea meditation at home, including handmade organic clay cups, Gaiwans, and bamboo infusers."
              Icon={Sparkles}
              className="col-span-3 lg:col-span-2"
            />
          </BentoGrid>
        </div>
      </section>

      {/* 4. Social Proof Marquee */}
      <section className="border-y border-neutral-200 bg-white py-12">
        <div className="mx-auto max-w-7xl px-6">
          <p className="text-center text-xs font-semibold uppercase tracking-widest text-neutral-400">
            Trusted by Teams & Tea Connoisseurs at
          </p>
          <Marquee className="mt-6 [--duration:35s]" pauseOnHover>
            {["Ottawa Tech Network", "Direct Family Farm Supply Chain", "Eventbrite Partner", "Drinkable Meditation"].map((company, i) => (
              <div
                key={i}
                className="mx-8 flex items-center justify-center font-sans text-sm md:text-base font-semibold tracking-wide text-neutral-400 hover:text-neutral-900 transition-colors"
              >
                {company}
              </div>
            ))}
          </Marquee>
        </div>
      </section>

      {/* 5. FAQ Accordion */}
      <section id="faq" className="bg-white border-b border-neutral-200/50 py-20 md:py-28">
        <div className="mx-auto max-w-4xl px-6 text-center">
          <BlurFade delay={0.05}>
            <div>
              <h2 className="font-sans text-3xl font-extrabold tracking-tight text-neutral-950 sm:text-4xl">
                Frequently Asked Questions
              </h2>
              <p className="mx-auto mt-4 max-w-2xl text-sm md:text-base text-neutral-500">
                Learn more about our brewing philosophy, ceremony bookings, and leaf sourcing.
              </p>
            </div>
          </BlurFade>

          <div className="mt-16">
            <Accordion items={faqItems} />
          </div>
        </div>
      </section>

      {/* 6. Contact Form Section */}
      <section id="contact" className="mx-auto max-w-4xl px-6 py-20 md:py-28 text-center">
        <BlurFade delay={0.05}>
          <div>
            <h2 className="font-sans text-3xl font-extrabold tracking-tight text-neutral-950 sm:text-4xl">
              Get in Touch
            </h2>
            <p className="mx-auto mt-4 max-w-2xl text-sm md:text-base text-neutral-500 mb-12">
              Have questions about public seat events or want to book an exclusive corporate workshop? Drop us a message.
            </p>
          </div>
        </BlurFade>

        <BlurFade delay={0.15}>
          <ContactForm />
        </BlurFade>
      </section>

      {/* 7. Footer */}
      <footer className="border-t border-neutral-200 bg-white py-12 text-center text-xs text-neutral-400">
        <p>© {new Date().getFullYear()} Chahaven. All rights reserved.</p>
        <p className="mt-1 text-[10px]">Ottawa, Canada · info@chahaven.ca</p>
      </footer>
    </main>
  );
}
