# Design explorations

Working files. Open the HTML directly in a browser — no server needed.

| File | What it is |
|---|---|
| `mark-responsive.html` | The two logomark sizes side by side, with the crossover point and a usage table |
| `logomark-variants.html` | How the mark was chosen: bezel vs standalone vs outlined |
| `logomark-characters.html` | The D-shape as mascot characters. Parked for possible animation work |
| `hero-options.html` | Headline options considered before "Run your recompiled ROM as a native app." |
| `discovery-animations.html` | Prototype animations of four discovery algorithms. Not wired into the site |
| `port1.png` | The reference photo crop the logomark geometry was measured from |

## The mark

Circle cut at 0.423× its radius below centre, corners filleted, three pins
spaced so all four gaps are equal. Every ratio measured from `port1.png`.

Two sizes, because the full mark stops working small:

- **Full** (bezel + insert) at 24px and up, and for the favicon, where an icon
  needs a recognisable silhouette.
- **Insert only** below ~20px. The bezel ring closes up and the pins lose
  separation, so the ring is dropped and the shape that carries recognition is
  scaled to fill the box.

Both ride `currentColor` with the pins knocked out via `fill-rule="evenodd"`,
so they invert on any background with no dark-mode rule.
