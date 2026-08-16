# Residential Architectural Styles of Town of Mount Royal

A single-page, mobile-friendly catalogue of the thirteen residential architectural
types defined by Town of Mount Royal's design-review by-law (PIIA By-law No. 1449,
2018), in English, illustrated with the by-law's own photographs.

**Live site:** https://sophiachen-geo.github.io/tmr-house-types/

## Structure

- `pages/` — the website itself (plain HTML and CSS, no build step)
  - `index.html` — the whole page
  - `img/` — photographs reproduced from By-law 1449
- `.github/workflows/deploy-pages.yml` — publishes `pages/` to GitHub Pages

## Publishing

GitHub Pages serves the `gh-pages` branch, which holds a snapshot of `pages/`.
The "Publish website to GitHub Pages" workflow refreshes that snapshot
automatically whenever `pages/` changes on `main` or
`claude/website-responsive-github-pages-qnvdpq`; it can also be run manually
from the **Actions** tab. There is no build step — edit `pages/index.html`,
push, and the site republishes itself. Don't edit the `gh-pages` branch by
hand; it is overwritten on every publish.

The layout is responsive and adapts to phones, tablets and desktops.
