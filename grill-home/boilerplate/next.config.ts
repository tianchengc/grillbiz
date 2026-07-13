import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "export",      // Static export — works with all 3 Cloudflare deploy options
  trailingSlash: true,   // Required for Cloudflare Pages static hosting
  images: {
    unoptimized: true,   // Required for static export (no Image Optimization API)
  },
};

export default nextConfig;
