# Landing zone toolchain reference

## Purpose

Record the tools, techniques, skills, and lessons from a previous scroll-driven landing page project, and say which of them to adopt, adapt, or skip for the knowledge-base landing zone.

Status: Draft
Audience: The maintainer and AI agents choosing tools for the landing zone
Page type: Reference
Maintainer: Unassigned
Last substantive review: Not independently reviewed; written 2026-11-19
Applicable versions: The reference project as described by the maintainer on 2026-11-19
Validation evidence: Source is the maintainer's description. Package availability and container tool versions were checked on 2026-11-19 (see [preflight](preflight.md)). No tool in this page was run for this knowledge base.
Known limitations: The reference project's scripts, skills, and documents were not available. Every measurement below is maintainer-reported and was not re-run. Client-specific names were removed on purpose.
Next review: When any tool is installed or the first design is built

## Reading this page

The reference project was a scripted landing page for a single property. Its hero was a short film that plays as the visitor scrolls. This knowledge base has different content, so each item gets a verdict:

- **Adopt**: use it as is.
- **Adapt**: keep the idea, change the details.
- **Optional**: only if the owner chooses a hero film.
- **Skip**: does not apply here.

## Where each tool runs

| Place | What runs there |
| --- | --- |
| Maintainer's Windows PC with a 16 GB AMD GPU (no CUDA) | The film chain: Real-ESRGAN and RIFE through Vulkan, ComfyUI on ROCm PyTorch, Qwen-Image-Edit, and Wan 2.2. |
| Google Flow, in a browser, with the maintainer's Gemini plan | The live film step. The maintainer signs in, uploads, and downloads; an agent can drive Flow's page and check the results. |
| This cloud container | Page build and checks only: Node, Playwright with Chromium, FFmpeg. It has no GPU, so the film chain cannot run here. |

## 1. Making a hero film (optional)

The chain turns real photographs into a scroll-driven film. Each step hands its output to the next. The governing rule was that everything in the film must come from real source photographs, and the AI may only change light and add motion.

| Step | Tool | Job | Verdict here |
| --- | --- | --- | --- |
| 1 | Source photographs | Keyframes and gallery images. | Skip. This knowledge base has no photographs, and the rule above forbids invented scenes. |
| 2 | Real-ESRGAN (4x upscaler, Vulkan) | Upscale small photos before cropping and upscale keyframes to 1920x1080. | Optional. Runs on AMD through Vulkan. |
| 3 | FFmpeg | Crop to 16:9, cut clips into frames, smooth flicker, sharpen, write WebP frames, the poster, and AVIF/WebP images. | Optional. Version 6.1.1 is in this container. |
| 4 | ComfyUI on ROCm PyTorch | Headless model runner, driven by a script and a launcher with Windows deadlock and memory-paging workarounds. | Optional. PC only. |
| 5 | Qwen-Image-Edit-2511 with a 4-step speed-up add-on | Relight each keyframe to one light state; every prompt ends by requiring the same composition. About 2 minutes per keyframe. | Optional. PC only. |
| 6a | Google Flow with Omni 1.2 Flash | Make each 8-second clip from a start image, an end image, and a camera-move prompt. | Optional. Preferred path. Needs upload to Google. |
| 6b | Wan 2.2 first-and-last-frame model on ComfyUI | Free, private fallback at 832x480, 1024x576, or 1280x720. | Optional. At 1080p it overflowed the 16 GB card. |
| 7 | Custom ComfyUI nodes | Encode first and last frames in tiles and split each render into two resumable jobs. | Optional. Fixed out-of-memory errors and VRAM leaks. |
| 8 | RIFE (Vulkan) | Measure real camera motion and retime frames to an even path at 48 fps. | Optional. Fixes the 8 Hz stutter in Wan output. |
| 9 | Pipeline scripts | One command runs every step from a film description file and redoes only what changed. A second prepares Flow's images and prompts. The import step thins each Flow clip to 81 frames and can reverse it. | Optional. Not present here; needs the reference files. |
| 10 | Review outputs | Before/after keyframes, contact sheets, join checks, a brightness chart, a motion chart. | Optional. Catches invented content, flicker, and lurching. |

Because the repository content policy rejects images and video, frame sets, posters, and gallery images would live in the website repository, never here.

## 2. Page and animation tools

| Tool or technique | Job | Verdict here |
| --- | --- | --- |
| Astro | Static site, almost no JavaScript. | Adopt. Already the [planned stack](../architecture.md). |
| Typed data file plus schema, checked at build | All copy, theme, and film settings live in data files; a missing field or translation fails the build. | Adapt. Use one landing-zone data file. The multi-client template aspect is not needed. |
| Film player, about 6 KB of plain TypeScript | Draws frames on a `<canvas>` as the visitor scrolls. | Optional. |
| Spring playhead | The shown frame follows scroll with a 240 ms spring on desktop, so wheel notches merge into one glide. | Optional. Biggest single smoothness gain. |
| Blending between frames | Blend the frames on either side of the playhead. | Optional. |
| Look-ahead and background decoding | Load 9 frames ahead and 3 behind, decode off the main thread, keep at most 14 frames in memory. | Optional. |
| Three frame sets | 1920, 1280, and 768 px wide; phones load every second frame; budgets of 50, 25, and 10 MB. | Optional. |
| Poster first | Nothing loads before the first scroll. Reduced-motion, `Save-Data`, and no-JavaScript visitors get only the poster. | Adopt the principle for any heavy media. |
| Focus per shot | Phones crop the film toward each shot's subject. | Optional. |
| CSS scroll-driven animations (`animation-timeline: view()`) | Slide-ups, image curtains, and parallax with no JavaScript. Never animates opacity. | Adopt. |
| `IntersectionObserver` | Fade-in fallback and count-up statistics for browsers without scroll-driven CSS. | Adopt as the fallback. |
| Hero overlays | Grain, vignette, progress bar with chapter ticks, a counter, a closing card. | Adapt. Keep only what helps reading. |
| Fontsource fonts | Self-hosted Archivo (125% width) and Inter Tight. | Adopt the self-hosting. Choose the typeface with the owner. |
| `<picture>` with AVIF and WebP plus blurred placeholders | Small images with a blurred preview. | Adopt if the design uses images. |

## 3. Quality checks

| Check | What it proves | Verdict here |
| --- | --- | --- |
| Data-file check | Landing data matches its schema. | Adapt. |
| `astro check` | Types. | Adopt. |
| Unit tests with `node --test` | Player guarantees: the spring, the frame window, the memory limits. | Optional, with the film player. |
| Playwright | Eight browser tests plus screenshots: no frames before first scroll, at most 14 frames, reduced motion, no JavaScript, phone overflow, a booking flow. | Adapt. Keep reduced motion, no JavaScript, and phone overflow. Replace the booking flow with search entry and topic navigation. |
| Lighthouse | Performance, accessibility, and best practices at 90, 95, and 90. | Adopt. |
| Smoothness check with a simulated mouse wheel | Turns "smooth" into a number and checks the exact frame is shown. | Optional, with the film player. |
| Tool health check | Every tool and model is installed. | Adapt. See [preflight](preflight.md). |

## 4. Claude Code skills and tools

| Item | Job | Port status |
| --- | --- | --- |
| Skill `hero-film` | Directing, producing, and reviewing a film. | Not in this repository. Needs the original file. Only useful if a film is chosen. |
| Skill `new-client-site` | Intake to preview for a new client. | Skip. This is a single site. |
| Skill `site-qa` | Runs every check plus desktop and phone screenshots. | Adapt. A draft is in the [landing zone design skill](../../../skills/landing-zone-design/SKILL.md). |
| Browser pane | Preview at desktop and phone sizes, and drive Flow. | Available only in the desktop app. In this container use Playwright with Chromium. |
| Launch configurations (site, ComfyUI) | One-click start of the dev server and ComfyUI. | Create once the website repository exists. |
| Documents: playbook, reference, film pipeline, animation guide, design guide, toolchain | Write down the process and lessons. | Adapt. Plan `DESIGN-GUIDE`, `ANIMATION-GUIDE`, and `TOOLCHAIN` documents in the website repository. |
| Codex owning a booking backend | Clear ownership split so prices and payments are never faked. | Skip. No booking flow exists. |

## Reported measurements from the reference project

These are the maintainer's figures. They show what was achievable, not what this knowledge base will achieve.

| Measure | Reported value |
| --- | --- |
| Lighthouse performance on the first view | 100 |
| Lighthouse bar | Performance 90 or more, accessibility 95 or more, best practices 90 or more |
| Motion unevenness, Flow clip versus raw Wan | About 2% versus 53% |
| Flow clip time | About 2 minutes for an 8-second 1080p clip |
| Wan at 1080p on a 16 GB card | 13 to 30 minutes per step, then a grey clip |
| Page weight budgets by frame set | 50, 25, and 10 MB |

## Lessons worth keeping

- Smooth motion depends on even timing as much as on frame count. Retime frames before judging.
- A spring on the playhead did more for perceived smoothness than any other change.
- Never animate opacity in scroll-driven CSS. Content can be left invisible if the animation does not run.
- Check every generated clip's first and last frame before use. The joins reveal invented content.
- Local 1080p video generation failed on a 16 GB card, so the pipeline moved to a hosted model.
- Make "smooth" a measured number. An opinion cannot gate a release.

## Related links

- [Landing zone design pack](README.md)
- [Design brief](design-brief.md)
- [Preflight and quality gates](preflight.md)
- [Website architecture](../architecture.md)
- [Upgrade hub](../../../README.md)
- [Back to root index](../../../../README.md)
