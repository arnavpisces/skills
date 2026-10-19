---
name: record-demo
description: Create or revise narrated product demo videos using real browser recordings, presentation-ready cursor and scroll motion, selective focus and zoom, and optional animated intros. Use for recording application walkthroughs, matching screen actions to a script, or editing an existing demo clip with fframes and local narration.
---

# Record Demo

Produce a replayable, evidence-grounded product video: narration, actual UI takes, an optional animated intro, editable composition, and a verified render. Support separate parts and surgical revisions; the user's requested review boundary determines how far to build.

## Start with scope and evidence

- Read the supplied narration and editor notes. Keep editor instructions out of spoken text. Identify what changes and what remains approved.
- Find the existing project, script, manifest, voice settings and delivered video before rebuilding. Preserve approved files in a separate revision directory.
- State the intended result and assumptions. Infer established theme, brand, voice and duration from the session. Ask only for information that materially changes the result and cannot be established from existing artifacts.
- Reuse the user's named, authenticated browser session. Let the user complete SSO. Do not relaunch or close a user-owned session as routine cleanup.
- Scout without recording. Match each spoken claim to a capability and state that actually works. Use existing approved records for consequential workflows. A recording request alone does not authorize production approvals, dispatches, cancellations, schedule changes, deletions, settings changes or notifications.
- Keep project output isolated from application source. Never package browser profiles, authentication state, credentials or secrets.

## Route the work

Read the relevant references as work reaches that stage:

- [Capture](references/capture.md): scouting, selectors, foreground tabs, human cursor, eased root/nested scrolling, repeatable takes. Copy/adapt [capture_runtime.py](scripts/capture_runtime.py) into the output project to avoid rewriting motion and recording mechanics.
- [Intro and composition](references/composition.md): animated intro storytelling, real-footage media APIs, focus masks, continuous zoom and timing.
- [Narration](references/narration.md): local Chatterbox generation, pronunciation, natural pacing, measured scene durations and audio QA.
- [Verification and delivery](references/verification.md): final encoded video/audio checks, revision provenance and source bundle.
- [Local Optimus example](references/optimus-local.md): this machine's proven project, voice runtime, session and visual identity. These are examples to verify, not universal defaults or proof of current UI state.

Use the installed `agent-browser` and `fframes-video` skills when available. Read `agent-browser skills get core` before browser operations, then inspect the installed command help. Inspect the actual Cargo version and media APIs instead of guessing from older examples. If a dependency is unavailable, report the concrete limitation and keep useful source work intact; do not substitute a reconstructed UI for requested real footage.

## Work in this order

1. **Scout and plan.** Inventory real views, reliable selectors, scroll containers and existing records. Create a shot list pairing narration with screen actions, pauses, focus regions and transitions. Check access to every linked app before takes.
2. **Narrate and time.** Generate only new or changed paragraphs. Measure the generated voice, preserve its natural pace, and derive the timeline from it. Fit a shorter target through concise wording when authorized, rather than accelerating the voice. Keep unchanged narration byte-for-byte when possible.
3. **Choreograph locally.** Write a fixed capture driver with readiness checks, timeouts, stable selectors and an explicit action allowlist. No LLM choices between movements during a take. Unexpected state, missing access, timing overrun or lost foreground ends the take.
4. **Capture separate takes.** Use a consistent 16:9 viewport and verify actual encoded pixels/fps. For this user's new demos prefer native 4K at 30 fps unless instructed otherwise. Record the visible cursor, leave clean editing handles, hold results for reading, and save clean screenshots. Test motion before the full sequence. Avoid heavy TTS, transcription and encoding jobs during browser takes.
5. **Compose.** Use actual MP4 footage, measured narration and restrained titles, camera motion and focus masks. Keep UI text readable. Label shortened processing waits explicitly. Preserve approved intro identity and unaffected scenes; render only the requested part.
6. **Verify and deliver.** Build and inspect from the generated Cargo project. Review pixels from the actual encoded export, validate audio separately, and deliver the MP4 with replayable source, clips, screenshots and final timing/script map.

## Editorial invariants

- Narration describes the action while it is visible: do not show a result before a sentence introducing its selection.
- Human motion is deliberate: roughly 400–800 ms pointer paths, a brief settle before click, 800–1400 ms eased scrolls, and 2–4 seconds on important results. These are pacing ranges, not reasons to override a supplied script.
- Scroll the actual container. Root scrolling, a Jira central pane and a nested results table are different targets. Resolve them during scouting.
- Begin a requested full-widget focus before zooming; retain a continuous zoom through scrolling and adjoining shots when specified. Avoid an automatic zoom-out between every widget.
- Separate camera motion, scrolling and highlight transitions enough to make their purpose clear. Avoid pointer wandering, incidental tooltips, jitter, repeated scrolls and unexplained jumps.
- Record real responses and real statuses. Use a clean edit or a visible “Wait shortened · real response” label when shortening a processing wait.
- A green focus mask tints surroundings while leaving the target UI clear. It must not alter values, statuses or answer text.
- Keep the final narration-to-screen map current after every revision. Report verification honestly; inspected frames/contact sheets are not a claim that the entire clip was watched in real time.
