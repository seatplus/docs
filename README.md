# Seatplus documentation

The source of the Seatplus documentation site. It is a [Next.js](https://nextjs.org) app that renders
Markdoc, built on the Tailwind UI "Syntax" template.

If you only want to write documentation, read
[Writing docs](src/pages/docs/contributing/writing-docs.md) — it covers the authoring rules that
this site actually enforces. This file covers running and maintaining the site itself.

## Running it locally

```bash
npm install
npm run dev
```

Then open <http://localhost:3000>.

Search is optional. Copy `.env.example` to `.env.local` and fill in Algolia DocSearch credentials if
you have them; without them the search button is hidden and everything else works normally. Do not
paste Algolia's public demo credentials — they work, which is the problem: they search Algolia's own
demo documentation rather than this site.

## Scripts

| Command | Does |
| --- | --- |
| `npm run dev` | Development server with hot reload |
| `npm run build` | Production build. **The only place Markdoc validation errors surface** |
| `npm run start` | Serve a production build |
| `npm run lint` | `next lint`. Covers JS/JSX only — it does not read `.md` files |

Run `npm run build` before opening a pull request. `npm run lint` will not catch a bad Markdoc tag, a
`callout` with an invalid `type`, or an `h3` placed before any `h2` — the build will.

## Layout

```
markdoc/            Markdoc schema: the custom tags and node overrides
public/images/      Screenshots and other page images, grouped by topic
scripts/            Maintenance scripts (see below)
src/components/     Site chrome. Layout.jsx also holds the sidebar navigation
src/pages/          The documentation itself. Every .md file here is a route
src/styles/         Tailwind, fonts, Prism and DocSearch styles
```

## Two things that surprise people

**The sidebar is defined in `src/components/Layout.jsx`, not in `Navigation.jsx`.**
`Navigation.jsx` is a renderer; the `navigation` array near the top of `Layout.jsx` is the data. A
page that is not listed there still resolves as a URL, but renders with no section eyebrow, no
sidebar highlight and no previous/next links. Adding a page is always two edits: the `.md` file and
that array.

**`pageExtensions` includes `md`, so any `.md` file under `src/pages/` becomes a live page.** There
is no routing configuration and no draft mechanism. Do not park work-in-progress `.md` files there.

## Screenshots

Screenshots come from the browser test suite in the
[`seatplus/core`](https://github.com/seatplus/core) package, not from manual captures. That keeps
them consistent, correctly sized, and refreshable when the interface changes.

To refresh them:

```bash
# in a seatplus/core checkout, with its dev services running
composer run browser

# back here
python scripts/import_screenshots.py
```

`scripts/import_screenshots.py` crops each full-page capture to its content — the raw captures are
1728×1117 regardless of how tall the page actually is — and copies the ones listed in its `MANIFEST`
into `public/images/`. Adding a new screenshot to the docs means adding a `snap()` call to the
browser suite in `seatplus/web`, then an entry to that manifest.

The script fails loudly if a manifest entry has no matching capture, so a partially-passing browser
suite cannot silently produce a docs build with missing images.

## Redirects

`next.config.js` holds permanent redirects for pages retired by the 2026 restructure. Those URLs are
linked from Discord history and elsewhere. Keep the entries; removing one breaks an external link.

## Licensing

Two licence files, deliberately:

- `LICENCE.md` — MIT, covering the documentation content in this repository.
- `LICENSE.md` — the Tailwind UI licence, covering the site template this project is built on.

Both apply. Neither can be removed.
