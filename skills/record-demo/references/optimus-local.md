# Local Optimus example — verify before reuse

These paths identify working sources on Arnav's machine, not assets bundled into this skill. They may move. Use `rg --files` in the stated parent directory if a path is absent. Do not depend on them for other products.

## Proven projects

Base: `/Users/arnav.kumar/Desktop/Optimus-AI-Video-20261001`.

- Approved natural 20-second intro: `optimus-ai-part1-intro-20s-natural.mp4`; source `src/part1_intro.rs`, `src/part1_intro_main.rs`, `generate_part1_concise_voice.py`, and `part1-intro/concise/`. Check the timing file referenced by the source before copying.
- Latest editor demo: `live-demo-editor-4k/`; delivery `optimus-ai-live-demo-editor-4k.mp4`, duration 140.4 seconds / 4,212 frames, native 4K at 30 fps.
- Curated standalone copy: `live-demo-editor-4k-delivery/`; assets `optimus-ai-live-demo-editor-4k-assets.zip`.
- Previous approved 155-second light-theme demo: `live-demo-light-4k/` and `optimus-ai-live-demo-light-4k.mp4`.

Within the latest project, useful starting points are `src/live_demo.rs`, `src/main.rs`, `live-demo/capture.py`, `record_all.py`, `generate_voice.py`, `prepare.py`, `make_score.py`, `check_speech.py`, `shot-manifest.json`, `script-with-screen-actions.md`, and `QA.md`. Read and adapt only what the new request needs; copying the older full driver would retain stale tab IDs/selectors/dates/record IDs.

The latest revision recaptured Home, shortened narration for sections 2 and 3, and reused integrated sections 4–11 byte-for-byte. This is the preferred surgical pattern when the user says the rest is good.

## Session and appearance

The user provided persistent session `optimus-demo`, profile `/Users/arnav.kumar/.optimus-demo-profile`, human input mode, headed Chromium, and application `https://prod-optimus.sprinklr.com`. Inventory existing tabs before reuse; do not launch a replacement when the session is already authenticated. If the user needs to start it again, the known command is:

```sh
agent-browser --session optimus-demo --headed \
  --profile "$HOME/.optimus-demo-profile" --input-mode human \
  open https://prod-optimus.sprinklr.com
```

The accepted takes used Optimus/Jira light theme, Voyager's native white task canvas, 1920×1080 CSS at 2× density, 30 fps, a visible human cursor and 1100 ms RAF scrolls. Themes/session login are not guaranteed to persist; verify them live.

Optimus Home root: `document.scrollingElement`. Known widgets included `#hw-lifecycle` and `#hw-sev`; tested Home scroll positions were 620, 900 and 1400 CSS pixels. Execution details used `.patching-host-table-wrap`; Jira used its central issue pane. All are prior selectors/coordinates to scout again, not current assurances.

No production approval, scheduling, dispatch, cancellation, rollback, deletion or notification is authorized by this skill. Show approved existing schedules, Voyager tasks, CAB tickets and execution outcomes. In the narrative, **Voyager is the execution layer**, while Optimus coordinates analysis, planning, governance and tracking. Automatically prepared CAB requests do not remove people's authorization role. Keep actual history success/failure counts and actual AI findings distinct from generalized claims.

## Local voice and build runtime

Chatterbox root: `/Users/arnav.kumar/chatterbox-tts`, Python `.venv/bin/python`, API `tts_runtime.py`, dictionary `pronunciations.json`. Later accepted voice settings are in [narration.md](narration.md).

Optional cached Whisper site-packages: `/Users/arnav.kumar/Desktop/Optimus-AI-Video-20261001/executive-review/whisper-env/lib/python3.11/site-packages`; models in sibling `whisper-models/`. Check paths and dependencies before reuse.

Rust environment: `/Users/arnav.kumar/.cargo/env`. Existing shared build cache is `BASE/target`; use `CARGO_TARGET_DIR` explicitly when reusing it, and still run commands from the new Cargo project. Never include that target cache or the authenticated browser profile in source delivery.
