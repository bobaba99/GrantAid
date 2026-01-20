import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  async rewrites() {
    return [
      {
        source: '/api/service/:path*',
        destination: 'http://localhost:8000/:path*', // Proxy to Python FastAPI
      },
    ];
  },
};

export default nextConfig;
