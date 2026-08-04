const withMarkdoc = require('@markdoc/next.js')

// Pages retired by the 2026 documentation restructure. Their URLs were public and are linked from
// Discord history and elsewhere, so each one permanently redirects to whatever now covers it rather
// than 404ing. Keep these entries; deleting one breaks an external link.
const retiredPages = [
  { source: '/docs/ssoScopes', destination: '/docs/concepts/sso-scopes' },
  { source: '/docs/controlGroup', destination: '/docs/concepts/permissions' },
  { source: '/docs/recruitment', destination: '/docs/recruitment/overview' },
  { source: '/docs/memberCompliance', destination: '/docs/personnel/observation' },
  { source: '/docs/corporationFeatures', destination: '/docs/personnel/member-tracking' },
  { source: '/docs/characterFeatures', destination: '/docs/character/assets' },
  { source: '/docs/serverFeatures', destination: '/docs/server-settings' },
]

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  pageExtensions: ['js', 'jsx', 'md'],
  experimental: {
    newNextLinkBehavior: true,
    images: {
      allowFutureImage: true,
    },
  },
  async redirects() {
    return retiredPages.map(({ source, destination }) => ({
      source,
      destination,
      permanent: true,
    }))
  },
}

module.exports = withMarkdoc()(nextConfig)
