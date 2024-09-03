const withNextra = require('nextra')({
  theme: 'nextra-theme-docs',
  themeConfig: './theme.config.tsx',
  latex: true,
})

module.exports = withNextra({
  output: "standalone",
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 's.wy.is',
        pathname: '/article-images/**',
      }
    ]
  }
})
