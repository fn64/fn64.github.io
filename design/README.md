# Design explorations

Working files from the logomark / copy / era-design work. Open the HTML files
directly in a browser — no server needed.

| File | What it is |
|---|---|
| `logomark-variants.html` | The chosen mark (bezel + D-insert) alongside the standalone D and outlined variants |
| `logomark-characters.html` | The D-shape as mascot characters (blob, mushroom, squid, ghost, spider, cat), three pinholes kept as eyes. Parked for animation work |
| `hero-options.html` | Six hero headlines that lead with what fn64 *is*. Current pick: "The layer under the game." |
| `hero-options-round1.html` | Earlier round, kept for the reasoning. Its "Ship it, fork it, embed it" line now serves as the closing CTA |
| `design-directions.html` | Six N64-era design directions paired against the current design, plus a deliberate cringe control |
| `era-palettes.html` | Five era palettes with hex values, each shown driving a hero, buttons, data table, and rating line |
| `discovery-animations.html` | Prototype animations of four discovery algorithms (delta-vote, prologue refinement, authority closure, `wrong == 0` grading) |
| `port1.png` | The reference photo crop the logomark geometry was measured from |

## Decisions made

- **Logomark** — circle cut at 0.423× its radius below centre, corners filleted,
  three pins spaced so all four gaps are equal. Every ratio measured from a
  photo of a real N64 controller port. Shipped as the bezel variant.
- **Vocabulary** — fn64 is a **runtime**. The five stages are a **pipeline**.
  The crates are a **stack**. `fn64-discover` is a **tool**. Upstream's README
  says "runtime" nine times and never "foundation" or "toolchain".
- **Stat claims** — two site stats contradicted upstream and were corrected.
  See the plan file for the citations.

## Open

- Palette direction (leaning Edge fifth-colour, with dev-doc treatment for the
  data table)
- Whether to build the era directions, and if so which
- Wiring `discovery-animations.html` into the real pages

## Research notes

Two findings drive the palette work, both from the magazines' own pages:

- **Edge printed its typefaces in every colophon**: ITC Franklin Gothic Heavy /
  Gill Sans Bold / Bell Gothic, plus a literal "Fifth colour: Pantone 8303c"
  spot plate beyond CMYK.
- **Edge had no score box.** The rating was one line at the foot of the last
  column, spelled as words ("Eight out of ten"), never a numeral. That is the
  model for presenting the recall figures.

EGM / GamePro / Game Informer typeface attributions were never confirmed —
treat any claim about those as unverified.
