"use client";
import React, { useState } from "react";
import { Send, Check } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { BlurFade } from "@/components/magicui/blur-fade";

export function BioContact() {
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
    <section id="contact" className="w-full px-6 mt-10">
      <BlurFade delay={0.4}>
        <div className="w-full bg-white/60 backdrop-blur-md border border-primary/10 p-6 rounded-2xl shadow-sm text-left relative overflow-hidden">
          {/* Subtle gold decoration line */}
          <div className="absolute top-0 left-0 right-0 h-[2px] bg-gradient-to-r from-transparent via-primary to-transparent" />

          <h3 className="font-serif text-xl font-semibold text-gray-900 mb-2">Send a Message</h3>
          <p className="text-xs text-gray-500 mb-6">Have questions or want to host a private group ceremony? Drop us a line.</p>

          <AnimatePresence mode="wait">
            {!submitted ? (
              <motion.form
                key="bio-contact-form"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                onSubmit={handleSubmit}
                className="space-y-4"
              >
                <div>
                  <label className="block text-[10px] font-semibold uppercase tracking-wider text-gray-500 mb-1">Name</label>
                  <input
                    type="text"
                    required
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    className="w-full px-3.5 py-2 border border-gray-250 rounded-lg text-xs bg-white/80 text-gray-900 focus:outline-none focus:border-primary transition-colors"
                    placeholder="Your Name"
                  />
                </div>
                <div>
                  <label className="block text-[10px] font-semibold uppercase tracking-wider text-gray-500 mb-1">Email</label>
                  <input
                    type="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="w-full px-3.5 py-2 border border-gray-250 rounded-lg text-xs bg-white/80 text-gray-900 focus:outline-none focus:border-primary transition-colors"
                    placeholder="you@example.com"
                  />
                </div>
                <div>
                  <label className="block text-[10px] font-semibold uppercase tracking-wider text-gray-500 mb-1">Message</label>
                  <textarea
                    required
                    rows={3}
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    className="w-full px-3.5 py-2 border border-gray-250 rounded-lg text-xs bg-white/80 text-gray-900 focus:outline-none focus:border-primary transition-colors resize-none"
                    placeholder="How can we help you?"
                  />
                </div>
                <button
                  type="submit"
                  className="w-full mt-2 flex items-center justify-center gap-1.5 rounded-full bg-primary text-white px-5 py-2.5 text-xs font-semibold hover:bg-primary/90 transition-all active:scale-[0.98] cursor-pointer"
                >
                  <span>Send Inquiry</span>
                  <Send className="h-3 w-3" />
                </button>
              </motion.form>
            ) : (
              <motion.div
                key="bio-success"
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0 }}
                className="py-8 text-center flex flex-col items-center justify-center"
              >
                <div className="h-10 w-10 rounded-full bg-primary/10 border border-primary/20 flex items-center justify-center mb-3">
                  <Check className="h-5 w-5 text-primary" />
                </div>
                <h4 className="text-sm font-semibold text-gray-900">Thank you, {name}!</h4>
                <p className="text-[11px] text-gray-500 mt-1 max-w-xs px-4">Inquiry sent successfully. We will get back to you at {email} shortly.</p>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </BlurFade>
    </section>
  );
}
