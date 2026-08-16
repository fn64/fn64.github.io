# fn64.github.io

The public site for [fn64](https://github.com/fn64/fn64). Two hand-written HTML
pages plus one stylesheet. No build step, no dependencies, no JavaScript.

## Before publishing

```sh
python3 scripts/lint-site.py
```

Enforces: exactly one `<h1>` per page, every local fragment resolves to a real
`id`, every referenced asset exists, meta description present.

## Styling: Tailwind v4, prebuilt and committed

Source is `src/app.css`. Output `styles.css` is **committed**, so GitHub Pages
still serves static files and the deploy workflow needs no build step.

### Rebuilding

```sh
curl -fsSL -o tailwindcss \
  https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-macos-arm64
chmod +x tailwindcss
./tailwindcss -i src/app.css -o styles.css --minify
```

Swap the asset name for your platform (`tailwindcss-linux-x64`, etc). The
binary needs no Node and is gitignored. CI rebuilds and fails on a diff, so
**if you edit markup or `src/app.css`, rebuild and commit `styles.css`** or the
build breaks.

### Rules

- Utilities in markup. Reach for `@theme` tokens (`text-ink`, `bg-paper`,
  `font-display`) rather than arbitrary values, so the palette stays governed.
- `@layer components` is only for what utilities genuinely cannot express.
  Currently three things, and they are why "no custom CSS at all" is not
  reachable:
  1. **Keyframes.** The hero word-cycle needs `@keyframes` with per-word
     `--delay` and `--accent`. `@theme static` keeps them from being
     tree-shaken, since no `animate-*` utility references them.
  2. **The logomark.** `.mark-body` / `.mark-pins` inherit `currentColor`, so
     the mark inverts on any background with no dark-mode rule. That
     inheritance is the whole trick — never hardcode those fills.
  3. **Geometry.** `clip-path` notches, SVG `fill`/`stroke`, grid-paper
     gradient.
- Do not add daisyUI or any component library. Verified: the standalone binary
  cannot load plugins (`@plugin "daisyui"` fails to resolve), so it would drag
  npm back in — and a themed component library fights the bespoke identity,
  which is the site's main asset.
- Browser floor is Safari 16.4+ / Chrome 111+ (Tailwind v4's baseline).
  Accepted deliberately for a developer audience.

## Voice

Write like a developer talking to other developers. The failure mode is copy
written *about* the project rather than *from inside* it.

**Do:**

- Name real things: `c_smoke`, `scripts/lane-parity.sh`, `fn64-abi`,
  `docs/ROADMAP.md`. A reader believes a file path.
- Give numbers with their caveat: "75.7–92.9% recall, graded not blind, each
  run uses a donor ROM and an answer key."
- State what is broken as plainly as what works: "audio is still broken (R5)."
  Hedges that name a specific gap are assets.

**Do not:**

- Write slogans that assert rather than inform. "Every claim has a test beside
  it" and "Trust is part of the pipeline" both got cut for this.
- Use the not-X-but-Y construction, or abstract-noun-plus-adverb
  ("Discovery fails honestly"). These read as written-to-be-quoted.
- Put an eyebrow kicker on every section. Keep them only where they name
  something greppable (`fn64-discover`) or a navigation state.
- Stack em-dashes doing the same corrective-clause job. Five in a row is a
  recognisable rhythm.
- Invent terms of art. "evidence contract" and "loud frontiers" appeared
  nowhere upstream.

**Vocabulary:** fn64 is a **runtime**. The five stages are a **pipeline**. The
crates are a **stack**. `fn64-discover` is a **tool**. Upstream's README says
"runtime" nine times and never "foundation" or "toolchain" — match it.

## Claims must be checkable

Every technical claim on the site should trace to the upstream repo. Two site
stats were once wrong because nobody checked:

- "Cold start — VPW2 passed without a decomp, answer key, or per-game
  configuration" contradicted `README.md`, which says the recall numbers are
  **not** cold-start.
- "5 / 5 tested AKI titles" misread `DISCOVER-PLAN.md`, where five refers to
  materialized *banks* in one game.

Before adding a number, find it upstream and cite where. Prefer claims that
cannot go stale (`wrong == 0` holds by construction) over ones that drift.

## API docs

Do not hand-write API reference. `fn64-abi` alone has 420 doc comments;
`cargo doc` output belongs on docs.rs, which builds automatically per release
and is where Rust developers look. The site hand-writes only what rustdoc
cannot generate: how the pieces fit, what boots today, what is still open.

## Deploy

`.github/workflows/pages.yml` stages only the real site files into `_site/`.
`design/` holds working explorations and is deliberately excluded — do not
publish it. The `paths:` filter uses globs so new pages deploy automatically.
