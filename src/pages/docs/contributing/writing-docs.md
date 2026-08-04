---
title: Writing docs
description: The authoring rules this documentation site enforces — the five available tags, how to add a page, and how screenshots are produced.
---

Documentation is the easiest place to start contributing to Seatplus: no PHP, no local instance, no EVE
application registration. This page is the complete set of rules for authoring it.

{% .lead %}

The site lives in [seatplus/docs](https://github.com/seatplus/docs). It is a Next.js app rendering
Markdoc.

```bash
git clone https://github.com/seatplus/docs.git
cd docs
npm install
npm run dev
```

{% callout type="warning" title="Run the build before opening a pull request" %}
`npm run lint` only reads JS and JSX — it will not look at a single `.md` file. Markdoc validation
errors surface **only** in `npm run build`. An invalid tag, a `callout` with an unsupported `type`, or
an `h3` before any `h2` all fail the build, and none of them fail lint.
{% /callout %}

---

## Adding a page

Two edits, both required:

1. Create `src/pages/docs/<path>.md` with frontmatter.
2. Add it to the `navigation` array in **`src/components/Layout.jsx`**.

The `href` must equal the file path minus `src/pages` and `.md`. It drives the sidebar highlight, the
previous/next footer, and the section name shown above the page heading.

{% callout type="note" title="An unlisted page is a dead end" %}
Because `pageExtensions` includes `md`, any `.md` file under `src/pages/` is immediately a live URL —
there is no draft mechanism. But a page missing from the `navigation` array renders with no sidebar
highlight, no section eyebrow and no previous/next links. It is reachable and orphaned at the same
time. Never add one without the other.
{% /callout %}

### Frontmatter

```yaml
---
title: Page title
description: One sentence describing the page, ending in a period.
---
```

`title` becomes the page heading and, unless `pageTitle` overrides it, the browser tab. Omit it and
the tab reads `undefined - Docs`. `description` becomes the meta description, so write it as a
sentence a search engine can show. Make `title` identical to the sidebar label you added.

---

## The five tags

This is the entire authoring vocabulary. Anything else is a build error.

### callout

```markdown
{% callout type="warning" title="Closing a posting keeps its applications" %}
Applications already submitted are not deleted, and remain in the reviewer queue.
{% /callout %}
```

`type` must be **exactly** `note` or `warning` — validation is strict and any other value fails the
build. There is no `info`, `tip`, `danger` or `caution`. Markdown inside the body works, including
code fences.

Use `note` for something helpful and `warning` for something that will cost the reader time, data or
trust if they miss it.

### figure

```markdown
{% figure src="/images/recruitment/job-portal.png" alt="The Job Portal listing one open posting" caption="The Job Portal. The badge shows whether the posting inspects the whole account." /%}
```

Self-closing. `src` is root-relative from `public/`, so `public/images/foo.png` is `/images/foo.png`.

**Always write a real `caption`.** Omitting it emits an empty `<figcaption>`, and a screenshot with no
caption makes the reader do the work of figuring out what they are looking at. The caption should say
what to notice, not restate the heading. `alt` is for people who cannot see the image; `caption` is
for everyone.

There are no width, height or lightbox attributes.

### quick-links

```markdown
{% quick-links %}
{% quick-link title="First run" icon="lightbulb" href="/docs/first-run" description="What a fresh instance needs." /%}
{% /quick-links %}
```

`icon` must be one of `installation`, `presets`, `plugins`, `theming`, `lightbulb`, `warning`. **Any
other value crashes the page render** — it is not validated, so the failure is a blank page rather
than a helpful error. Adding a new icon means adding a component under `src/components/icons/` and
registering it in `src/components/Icon.jsx`.

### link

```markdown
{% link href="/docs/admin" %}Administration tasks{% /link %}
```

Prefer a plain markdown link — `[Administration tasks](/docs/admin)` — which renders identically and
is easier to read. The tag buys nothing.

### The lead annotation

`{% .lead %}` on its own line after the opening paragraph styles it as an introduction. Use it once
per page, at the top.

---

## What this site does not have

Do not reach for these; they do not exist and there is no way to add them without changing the
Markdoc schema:

- tabs or any OS/method switcher;
- code groups or multi-file code blocks;
- partials, so shared content must be linked rather than included;
- variables, so version numbers are hardcoded on every page that names one;
- line highlighting, line numbers, filenames or copy buttons on code fences;
- callout types beyond `note` and `warning`;
- steps, accordions, badges, tables of parameters, or embedded video.

Code fences take a bare language and nothing else — open with three backticks followed by `shell`,
`dotenv`, `json` or similar, and close with three backticks.

Writing ```` ```{2-4} ```` does not highlight lines 2 to 4 — `{2-4}` is parsed as the *language*, and
the block renders with no highlighting at all.

GFM pipe tables **do** work, and are the right tool for permission lists, status values and field
references. Keep cells short: a long paragraph in a table cell overflows badly on a phone.

---

## Headings

- Only `h2` (`##`) and `h3` (`###`) appear in the "On this page" panel. An `h4` is invisible.
- **An `h3` before any `h2` throws a build error.** Never open a page with `###`.
- Heading ids are generated by lowercasing and hyphenating, so `## Database backups` becomes
  `#database-backups`. Two identical headings on one page get a numeric suffix silently — rename one
  instead.
- Sentence case, no trailing colons.

---

## Links

**Always write internal links absolute**, starting `/docs/`. A relative `href` resolves against the
current directory, which is how this site accumulated four broken links: `{% link href="admin" %}` on
a page under `/docs/contributing/` points at `/docs/contributing/admin`, which does not exist.

When you retire or move a page, add a redirect to `next.config.js` rather than letting the old URL
404. Documentation URLs get pasted into Discord and stay there for years.

---

## Screenshots

Screenshots are **not** captured by hand. They come from the browser test suite in the
`seatplus/core` package, which drives a real instance and captures each view. That is what keeps them
consistent with each other and refreshable when the interface changes.

To refresh every image:

```shell
# in a seatplus/core checkout
composer run browser
```

```shell
# in this repository
python scripts/import_screenshots.py
```

The script crops each capture to its content — the raw captures are 1728×1117 regardless of how tall
the page really is — and copies the ones named in its `MANIFEST` into `public/images/`.

To document a screen that has no screenshot yet:

1. Add a `snap($page, 'my-view')` call to the relevant browser test in the `seatplus/web` package.
2. Run the suite in `seatplus/core` to produce `my-view-desktop.png`.
3. Add `'my-view': 'section/my-view.png'` to the `MANIFEST` in `scripts/import_screenshots.py`.
4. Run the import script and reference `/images/section/my-view.png` in your page.

Only the desktop captures are used. The suite also produces iPhone captures, which the docs do not
currently ship.

---

## Style

- Second person. "You open the posting", not "the user opens the posting".
- No "simply", "just" or "easily". If it were simple the reader would not be reading this.
- Name the exact permission and the exact ESI scope a feature needs. That is almost always the
  question the reader actually arrived with.
- State surprising behaviour plainly in a `warning`, including when it is unflattering. The
  documentation's job is to stop someone losing an afternoon, not to make the software look good.
- Do not document behaviour you have not verified in the code. A confident wrong sentence is worse
  than an honest hedge.
