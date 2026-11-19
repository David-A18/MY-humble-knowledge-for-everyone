# Knowledge spiral concept and build plan

## Purpose

Define the landing zone concept the owner chose, the knowledge spirals, and the plan to build it: interaction states, visual system, the role of AI-generated video, the topic reading view, and phased delivery with exit criteria.

Status: Draft
Audience: The maintainer and AI agents designing and building the landing zone
Page type: Design specification and plan
Maintainer: Unassigned
Last substantive review: Not independently reviewed; written 2026-11-19
Applicable versions: Catalog of 2026-11-19 (290 concepts); prototype version 2
Validation evidence: A working prototype was built and driven in headless Chromium (software WebGL) at 1440x900 and 390x844 in dark and light themes. The full flow ran with no console errors and no horizontal overflow. No real GPU, real phone, screen reader, or reader test was used.
Known limitations: The prototype is a single HTML page, not website code. Generated video has not been produced yet. Timings and budgets below are design targets until measured on real devices.
Next review: After the reference clips are generated and the prototype is tuned

## The concept

The knowledge base is drawn as glowing spirals floating in space. The owner supplied two reference images: a dark version (deep space with violet, pink, red, and orange nebulae) and a light version (soft white paper tones with pink and gold light). Both show the same structure:

| Element in the image | Meaning in the knowledge base |
| --- | --- |
| Central vertical line (white-gold glow) | The knowledge base itself, which connects everything |
| A spiral wrapping the line (gradient ribbon: yellow, orange, red, pink, violet) | One principal section: AI, Cloud & Platform, or Tech News |
| One loop of the spiral | One section inside it, such as AWS, Kubernetes, or Security |
| Paper pages orbiting the loop | The topics (concept pages) of that section |
| Sparkles, dust, and light trails | Atmosphere only; they carry no data |
| Concentric rings at the base | The ground each spiral stands on; atmosphere only |

The reference images cannot be stored in this repository, because the content policy accepts text only. They live with the owner and, later, in the website repository.

## Current mapping

The prototype builds this map from `generated/knowledge-catalog.json` with [spiral-map-prototype.py](spiral-map-prototype.py), so every page shown is a real concept with its real title, status, and description. All 290 catalog concepts are placed.

| Spiral | Loops (pages) |
| --- | --- |
| AI | AI tools and MCP (3), Knowledge bases (7), RAG (6) |
| Cloud & Platform | AWS (57), Kubernetes (94), Terraform (16), Git (20), DevOps (7), FinOps (8), Databases (12), Migrations (12), Security (3), Multi-cloud and edge (6), Cross-topic guides (19), Architecture and languages (2) |
| Tech News | AI news (2), Security news (1), Economy (1) |
| Library, outside the spirals | Start here, glossary, decision records, and templates (14) |

Mapping rules to keep:

- The map is a small configuration file read at build time. Counts always come from the catalog.
- A new top-level area must be assigned to a spiral, or the build fails. Silent omission is not allowed.
- News loops group briefs by topic tag. The News spiral grows each week, so it must look good with very few pages.
- Kubernetes (94 pages, including Crossplane) is too large for one comfortable loop. The loop view needs filter chips by subfolder, such as Crossplane, Troubleshooting, and Commands.

## Interaction states

### 1. Overview (arriving on the landing zone)

- The three spirals draw themselves upward from their bases over about 2.2 seconds, then the pages fade in from the bottom loop to the top. This is the one orchestrated moment.
- Pages ride along their own loop, bob gently, and flutter. Each loop shows a sample of up to four to six pages.
- Hovering a loop brightens that loop and shows a tooltip with the section name and page count.
- Hovering a page makes it shine (a warm halo), grow, and spin, and shows its title, section, type, and status.
- The camera follows the pointer with gentle parallax and a slow sway.
- Each spiral has a label under its base: name, number of sections, and number of pages.
- Phones show one spiral at a time. Swiping sideways or using the tabs changes spiral.

### 2. Loop focus (after clicking a section)

- The camera flies to that loop. Other spirals and loops dim to near black.
- Every page of the section leaves the ribbon and expands into a helical turntable around the loop, with the nearest pages arriving first.
- Scrolling, dragging, or the arrow keys turn the turntable. Pages move left or right and slightly up or down along the helix, and tilt with the speed of the turn.
- The turn uses a critically damped spring of about 0.5 seconds, and snaps to the nearest page when scrolling stops. This applies the reference project's lesson that a spring on the playhead matters most for smoothness.
- A caption shows the front page: position (for example 07 / 94), title, and status.
- The back button, Escape, or the brand returns to the overview. The pages fly back into the ribbon.

### 3. Topic preview (hover or click a page)

- Hover: shine, spin, and a tooltip with the title. A spinning page stays hovered while the cursor remains inside its footprint, so it does not flicker when it turns edge-on.
- Click: the page turns to the front, and a preview card opens with the section, title, description, status, type, and a link.
- In the website, the link goes to the page's route. In the prototype, it opens the source file on GitHub.

### 4. Topic reading (on the topic page)

- All animation stops. The scene is paused and its WebGL context is released, so the reading page is light and calm.
- The page uses a reading layout: a 65-character line, clear headings, a table of contents, code blocks, and the trust panel (status, maintainer, sources, freshness, source commit).
- A small static spiral breadcrumb shows where the page sits: spiral, loop, and position.
- A "Continue exploring" block offers neighbours in the same loop, authored related links, and one page from another spiral. This keeps the discovery feel without animation.
- The transition into the topic uses the View Transitions API: the clicked page grows into the article. Going back restores the loop and turntable position.

## Inputs and accessibility

| Input | Overview | Loop focus |
| --- | --- | --- |
| Mouse | Hover loop or page; click to open | Wheel turns; hover and click pages |
| Touch | Tap a loop or page; swipe to change spiral | Drag turns; tap a page |
| Keyboard | Tabs, labels, and Browse are focusable; `/` opens Browse and search | Left and right arrows turn; Enter previews; Escape goes back |

- The full site works without the 3D scene. Browse and search is an HTML list of every page with real links. The website must render this list as server-side HTML, so it also works without JavaScript.
- If WebGL is unavailable, the list opens automatically with a short note.
- Reduced motion: no intro, no drift, no spin, instant camera moves. Hover and click still work.
- `Save-Data` or a low-power device: no bloom, fewer particles, and the poster loop described below instead of the live scene, unless the visitor asks for it.

## Visual system

| Token | Dark (space) | Light (paper) |
| --- | --- | --- |
| Background | `#07060b` with violet and ember nebulae | `#f4f2f6` with pastel pink and gold haze |
| Text | `#f4eee6` | `#1c1524` |
| Muted text | `#a99fb3` | `#675c72` |
| Gold (trust and actions) | `#ffcf7a` | `#a86a0c` |
| Ember (Cloud & Platform) | `#ff7a3d` | `#c94a12` |
| Violet (AI) | `#b36dff` | `#7436cf` |

- Each spiral has its own gradient within the shared palette: AI runs rose to violet; Cloud & Platform runs yellow through orange, red, and pink to violet (the reference gradient); Tech News runs white-gold to orange.
- Type: Archivo at 125% width in uppercase for display (the expanded-capitals look from the reference project), Inter Tight for text, and JetBrains Mono for labels and counts. The website self-hosts these fonts.
- Glass panels (blurred, translucent) for the interface; the spirals are the only loud element.
- Bloom applies to the dark theme only and stays below page brightness, so pages shine without washing out. The light theme uses normal blending.
- Status chips: `draft` is outlined and quiet; `stable` is filled gold. The footer states the real counts and says drafts are not yet fully reviewed.

## Why the interactive scene is real-time, and where Gemini video fits

A video cannot be the interactive landing zone. Pages in a video cannot be hovered or clicked one by one. A video also cannot follow the catalog as pages are added, switch theme, or zoom into any of 18 loops. The interactive scene is therefore rendered live with WebGL (Three.js), as in the prototype.

Generated video still has four useful jobs:

| Use | What it gives |
| --- | --- |
| Motion and look reference | Target clips to tune the live scene: how pages flutter, how light flows along the ribbon, how the zoom should feel |
| Poster loop | A short silent loop for reduced-data, low-power, and no-WebGL visitors, and the first frame before the scene loads |
| Announcement teaser | A shareable clip and social preview image for the launch |
| Nebula plate (optional) | A slow, seamless nebula background behind the live scene, if shader nebulae look too flat |

### Gemini production kit

Generation runs either through the Gemini API with a key the owner provides, or in Google Flow with the owner signed in. Each clip is 8 seconds.

| Shot | Start frame | Prompt summary |
| --- | --- | --- |
| V1 Hero, dark | Clean dark keyframe | Slow orbit around a glowing white-gold vertical beam wrapped by a gradient light ribbon (yellow, orange, red, pink, violet); translucent paper pages orbit and flutter along the ribbon; sparkles flow upward; deep space with violet and ember nebulae; no text, no logos; keep the exact same composition and colours. |
| V2 Hero, light | The light reference image | The same motion on a soft white background with pink and gold light; white paper pages; no text, no logos. |
| V3 Hover | A close crop of one page and the ribbon | One page catches the light, brightens with a warm halo, and spins once around its vertical axis; everything else keeps drifting slowly. |
| V4 Zoom into a loop | Mid-height crop of the spiral | The camera pushes into one loop; pages multiply and fan out into a ring around the beam; other loops fall dark. |
| V5 Nebula plate | A nebula-only frame | A seamless, very slow drift of violet and ember nebulae with stars; no foreground objects. |

Preparation and review:

1. The dark reference image contains annotation text and a colour legend. Remove them first (Gemini image editing), and extend both references to 16:9 for desktop. Keep 9:16 versions for phones.
2. End every prompt with: keep the exact same composition, no new objects, no text.
3. Check the first and last frame of every clip, and watch for invented text on the pages, colour drift, and stutter. Measure motion evenness before use.
4. Store clips, frames, and posters in the website repository only. This repository accepts text only.

## Performance budget

- Render HTML first. Load the scene after the first paint and only on capable devices.
- Three.js and the scene code: no more than about 200 KB compressed. Data map: no more than about 100 KB.
- Pixel ratio capped at 1.75. Bloom at half resolution. Pause rendering when the tab is hidden or the scene is off screen.
- Targets: 60 frames per second on a desktop, at least 30 on a mid-range phone. Measure on real devices before launch.
- Lighthouse targets from the [preflight](preflight.md) still apply.

## Build phases

| Phase | Work | Exit criteria |
| --- | --- | --- |
| 0. Decisions | Owner chose interactive spirals in both dark and light themes; spirals are AI, Cloud & Platform, and Tech News | Done 2026-11-19 |
| 1. Prototype | Single-page WebGL prototype from real catalog data | Done: flow works in Chromium at desktop and phone size, both themes, no console errors |
| 2. Reference clips | Clean keyframes, then V1 to V5 with Gemini | Clips reviewed against the checklist above |
| 3. Tune | Match the prototype's motion, density, and colour to the clips; add Kubernetes filter chips; tune small laptop widths | Owner approves the look on a real screen |
| 4. Website scaffold | Astro site, scene as a lazy-loaded island, spiral map config checked at build | Builds from a pinned commit; fails on an unmapped area |
| 5. Topic page | Reading template, trust panel, spiral breadcrumb, continue exploring, view transition | Works without JavaScript; passes the accessibility scan |
| 6. Fallbacks | Server-rendered browse list, poster loop, reduced-motion and `Save-Data` paths | Each path tested in Playwright |
| 7. Quality gates | Preflight gates plus frame-rate checks on real devices and WebGL-off tests | All gates pass |
| 8. Launch and learn | Deploy, then run reader tasks | Reader results recorded; navigation adjusted |

## Prototype version 2: cinematic renderer

The owner judged version 1 too simple ("like a game on low graphics"). Version 2 keeps the concept and controls and rebuilds the rendering to match the reference image:

| Layer | Technique |
| --- | --- |
| Camera | Close on one spiral at a time, like the reference composition; scrolling climbs the spiral; the other spirals stand far behind for depth; an "All" view shows the three together |
| Ribbon | A real 3D band whose width lies on the spiral surface, so it narrows at the silhouette; animated plasma noise, a white-hot core, bright edges, and travelling streaks |
| Glow | A wide soft halo band, two light filaments wrapping the ribbon, and HDR bloom that only catches values above white |
| Pages | Paper textures drawn with each topic's real section, type, title, summary, and status; curl and flutter in the vertex shader; backlit tint from the ribbon colour at that height; luminous edges |
| Beam | White-gold core with travelling energy pulses, a star flare, and an anamorphic streak at the top |
| Base | A swirling vortex disk, a hot point, and seven slightly tilted orbit rings with travelling sparks |
| Particles | Ribbon dust streams, ambient dust, and star-shaped sparkles with diffraction spikes |
| Background | A high-quality domain-warped nebula rendered once into a texture, plus a star field with diffraction spikes on bright stars |
| Finish | ACES tone mapping in the dark theme, slight chromatic aberration, vignette, and film grain |
| Navigation | A section rail on the right lists every loop; hovering a tick moves the camera to it and clicking enters it |

The Gemini step in phase 2 is still open: this cloud session has no browser and no API key. The generated clips will serve as the tuning target and the poster loop, as planned above.

## Known issues

- The Cloud & Platform spiral is tall (12 loops). Climbing works, but the intro could travel the whole spiral once.
- The AI and Tech News spirals are short. They should still look complete with very few pages.
- Touch has no hover state. A tap goes straight to the preview card, which is intended, but needs a reader test.
- Software WebGL was used for checks. Real-GPU frame rates are unknown, and the renderer needs a low-power profile (no filaments, fewer particles, no bloom) before launch.

## Related links

- [Landing zone design pack](README.md)
- [Design brief](design-brief.md)
- [Toolchain reference](toolchain.md)
- [Preflight and quality gates](preflight.md)
- [Website requirements](../requirements.md)
- [Upgrade hub](../../../README.md)
- [Back to root index](../../../../README.md)
