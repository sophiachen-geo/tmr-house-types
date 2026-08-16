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

The site deploys automatically via GitHub Actions: every push to `main` or to
`claude/website-responsive-github-pages-qnvdpq` republishes it. It can also be
redeployed manually from the **Actions** tab ("Deploy website to GitHub Pages" →
"Run workflow"). There is no build step — edit `pages/index.html` and push.

The layout is responsive and adapts to phones, tablets and desktops.
