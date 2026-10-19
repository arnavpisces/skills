---
name: create-flowchart
description: Use when creating or editing D2 flowcharts, especially when the diagram needs structured title/description placement, compact whitespace, embedded fonts, or rendered visual verification.
---

# Create Flowchart

Create the `.d2` source and a rendered SVG; keep the source readable and the output reproducible.

## D2 reference and basic usage

D2 is the text-to-diagram language in the official [d2lang/d2 GitHub repository](https://github.com/d2lang/d2). Use the [D2 Tour](https://d2lang.com/tour/intro/) and [cheat sheet](https://d2lang.com/tour/cheat-sheet/) as the primary syntax references. Install the CLI with the official installer or `go install github.com/d2lang/d2@latest`; if neither is available, use `go run github.com/d2lang/d2@latest`.

The minimal workflow is:

```bash
printf 'start -> decision -> finish\n' > input.d2
d2 input.d2 output.svg
```

Use named objects for readable source and labeled connections for decisions:

```d2
refresh: Refresh inventory
validate: Validate response
refresh -> validate: valid
validate -> failed: error
```

D2 supports SVG, PNG, and PDF exports. Choose the layout engine deliberately; ELK is a good default for directed node-link flows with routed branches.

## Visual defaults

- Create the flowchart only by default. Do not add a standalone title, subtitle, description, footer, or other surrounding copy unless the user explicitly asks for it.
- Use `direction: right` by default so the flow reads left to right. If the user requests a top-down page composition, use `direction: down` at the graph root and route branches without crossing nodes.
- Use a restrained professional palette: dark navy text (`#17233E`), pale blue for primary/process nodes, pale amber for validation/decision nodes, pale green for success, pale red for failure, and cool gray for operational/status nodes. Keep fills light, strokes darker, and use one consistent stroke width.
- If a box has a title or heading, write that title in ALL UPPERCASE and bold it. Keep supporting body text in normal sentence case and regular weight unless the user requests otherwise.

## Structure and layout

- If the user explicitly requests a title or description, treat it and the flow as one visual composition. D2's ELK engine treats disconnected text nodes as separate graph components, which can place copy far left of the flow and create large empty space.
- For explicitly requested surrounding copy, render the flow with `--pad 0`, then compose the copy into the same SVG coordinate system above the flow's actual left edge. Expand both the outer and nested SVG `viewBox`/height to include any translation; otherwise bottom cards can be clipped.
- Prefer ELK for routed branches. Do not use a grid merely to align the header: grid layouts can collapse branch edges into straight-through lines.
- `near: top-left` anchors to the canvas, not necessarily to the first card. `near: <other-shape>` is not supported by ELK.
- Keep whitespace intentional: crop the rendered canvas, use small padding, and visually inspect the full output—not only the default browser viewport.
- D2 does not interpret inline Markdown such as `**TITLE**` inside ordinary labels; it renders the asterisks literally. For a title plus supporting copy, use a container node with separate title/detail children. Set `title.style.bold: true` and `detail.style.bold: false`; use `vertical-gap: 0` only when compact spacing is desired.
- For top-down ELK diagrams, keep direction global: do not rely on per-card `direction` overrides. Use `grid-columns: 1` inside each card to stack its title and detail. For reliable left/right padding, make both rows transparent fixed-size rectangles with the same width and explicit, font-appropriate heights, for example:

  ```d2
  step: {
    label: ""
    grid-columns: 1
    vertical-gap: 10
    grid-gap: 0
    title: STEP { shape: rectangle; width: 420; height: 40; style: { fill: transparent; stroke: transparent; stroke-width: 0; bold: true; font-size: 26 } }
    detail: "Supporting description" { shape: rectangle; width: 420; height: 30; style: { fill: transparent; stroke: transparent; stroke-width: 0; bold: false; font-size: 20 } }
  }
  ```

  The outer card retains the semantic fill and border, while the transparent rows center text inside a padded content area. Increase row width for horizontal breathing room and row heights only enough to prevent vertical border contact; recheck page dimensions after every change.
- Within a related family of diagrams, use the same card structure for every node. If the reference uses `label: ""` with `title` and `detail` children, convert single-line nodes to that structure too; mixing direct labels and child text can produce different font embedding, card heights, and visual weight across the set.
- Prevent text overflow by letting D2 size the outer box from its text children. For long titles or details, use explicit line breaks (`\n`) or separate `title`/`detail` text children rather than forcing a one-line label into a fixed box. If a fixed `width` or `height` is necessary, render and inspect it at the requested font before keeping the constraint.
- When repairing existing diagrams, audit the `.d2` source first: every declared node and labeled edge must still be represented in the regenerated SVG. A suspiciously short SVG height for a multi-line flow is evidence of a stale or incorrectly rendered artifact; re-render from the source instead of hand-editing the SVG geometry.

## Branching patterns

Choose the topology from the behavior being explained; do not force every diagram into a simple chain.

- Use a linear spine for a genuinely sequential process.
- Use a decision split when one step has mutually exclusive outcomes. Make the decision/router an explicit node and label each outgoing edge with a short condition or outcome.
- Use fan-out/fan-in when one input is handled by several parallel domains or services. Keep parallel branches in the same visual band and rejoin them at a named aggregation or contract node when the process converges.
- Use a validation or retry loop when a failed check returns to a bounded repair, fallback, or re-submission step. Route the loop above or below the spine, label it, and avoid edges through other cards.

For a branched D2 source, prefer named nodes and explicit edges so the graph remains auditable:

```d2
request: REQUEST
route: ROUTE REQUEST
deterministic: DETERMINISTIC PATH
planned: MODEL-PLANNED PATH
request -> route
route -> deterministic: DETERMINISTIC
route -> planned: MODEL-PLANNED
```

Keep one dominant spine in the requested direction. Branches should leave a clear router/decision node, use intentional orthogonal routing, and either terminate at a meaningful outcome or rejoin at a named result. Avoid crossing edges, detached condition labels, unexplained back-edges, and decorative branches. A diagram may use nested grouping or a decision diamond when it improves semantics, but every visual distinction must correspond to a real behavior.

Before rendering, perform a branch audit: enumerate every source node, destination node, and edge condition from the `.d2` file; check that success, failure, fallback, and retry outcomes are represented; then confirm the SVG contains the same visible nodes and routes. For multi-branch diagrams, inspect both the full canvas and a natural-size view so thin routed edges and labels are not hidden by scaling.

## Fonts

- D2 embeds fonts through CLI flags, not diagram CSS. Supply the actual TTF for every used style: `--font-regular`, `--font-italic`, `--font-bold`, and `--font-semibold`.
- When Google Sans is requested, use an available Google Sans/Google Sans Flex TTF and preserve it beside the artifact with its license. Do not claim a CSS `font-family` change is sufficient when D2 has embedded its default font.
- Verify the generated SVG contains D2's embedded font-face declarations and that browser rendering matches the requested family.
- When only a Google Sans variable TTF is available, D2 may embed the regular default for both `--font-regular` and `--font-bold`. After rendering, run `scripts/enable_google_sans_bold.sh <output.svg>` to make title text request the embedded regular variable face at `wght: 700`. Verify in the SVG that `.text-bold` contains both `font-weight: 700` and `font-variation-settings: "wght" 700`.

## Render and verify

Use D2's CLI, for example:

```bash
d2 input.d2 output.svg --pad 0 \
  --font-regular fonts/GoogleSans.ttf \
  --font-italic fonts/GoogleSans.ttf \
  --font-bold fonts/GoogleSans.ttf \
  --font-semibold fonts/GoogleSans.ttf

scripts/enable_google_sans_bold.sh output.svg
```

For a directory of related flowcharts, render each canonical `.d2` file one-to-one to its matching `.svg` with the same ELK, padding, and font flags. Keep source edits and output regeneration separate so missing branches can be reviewed before visual QA. Do not add standalone title or description nodes to a flowchart-only artifact.

If `d2` is unavailable, `go run github.com/d2lang/d2@latest` is an acceptable local fallback. After every output change:

1. Validate compilation and SVG/XML structure.
2. Open the local SVG with `agent-browser` and capture a full-page screenshot. For a batch, a temporary contact sheet is useful for coverage, followed by focused full-size checks of branched or multi-line diagrams.
3. Inspect the screenshot for clipped cards, overlaps, branch routing, header alignment, and excess whitespace.
4. Confirm the visible text has deliberate left/right and top/bottom breathing room inside each border at the exact embedded font, especially long detail lines and the bottom-most node. Also confirm the SVG `viewBox` includes every node and routed edge.
5. Fix the source or compositor and repeat until the entire diagram is visible.

Success means the output contains only the requested flowchart direction, box titles are uppercase, colors look professional and semantically consistent, the flow has no accidental whitespace, padded card text remains legible, all branches remain legible, the requested font is embedded, and no node is clipped. If surrounding copy was explicitly requested, it must align with the first flow card.
