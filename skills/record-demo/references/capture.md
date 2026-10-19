# Real UI capture

## Scout before takes

Load the installed CLI guide and inspect supported options:

```sh
agent-browser skills get core
agent-browser --version
agent-browser mouse --help
agent-browser record --help
agent-browser set --help
agent-browser type --help
```

Use the user's existing named session for tab inventory and inspection. Authentication remains in that profile; reuse it in place. Record selectors, target text/state, tab IDs, exact root or nested scroll containers, target scroll positions, focus rectangles and expected link destinations. Prefer stable IDs/data attributes/CSS selectors over snapshot refs that may change on navigation. Confirm tabs and selectors again before recording; do not hardcode an old tab ID as current truth.

Check every destination, including linked execution and approval systems. If SSO blocks one scene, complete independent preparation and let the user authenticate; do not record the login or invent the missing scene.

For each shot specify preconditions, timed actions, resulting evidence, narration, focus/zoom, reading holds, output filename and editing handles. Pre-position and wait for chart/table hydration off-take. Do not scroll the body when the visible content is inside a pane.

## Resolution and theme

The proven 4K arrangement is **1920×1080 CSS at deviceScaleFactor 2**, yielding **3840×2160 actual recording frames**, with readable desktop layout. A 3840-wide CSS viewport can shrink text and reflow the app; do not assume it is visually better. For Full HD, native 1920×1080 at density 1 may be appropriate. Check supported CLI syntax, actual `innerWidth`, `innerHeight`, `devicePixelRatio`, and then encoded MP4 dimensions/fps with `ffprobe`. A 4K export upscaled from a 1080p take is not native 4K.

Use the requested theme consistently across apps. Verify it rather than silently changing settings; an explicitly requested appearance change is within scope. Keep the tab foregrounded, check `document.hidden`, and stop if it loses foreground.

## Fixed choreography

Copy `../scripts/capture_runtime.py` beside the project-specific driver. It exposes a session-bound `Capture` helper and `Action` records; it does not discover pages or generate a demo automatically. Populate hostnames, selectors, preconditions, theme checks and parking coordinates from scouting. Add explicit post-click readiness checks and app-specific logic in the driver. Its selector allowlist is a guardrail, not a sandbox for arbitrary `eval` calls.

Example structure after scouting (selectors and domain shown here are illustrative):

```python
from pathlib import Path
from capture_runtime import Capture, Action

c = Capture(session="demo", output=Path("capture"),
            allowed_hosts={"demo.example.com"},
            allowed_clicks={"#nav-home"}, required_state="true")
c.activate("t1")  # replace with current tab inventory
c.ready("!!document.querySelector('#metrics canvas')")
c.scroll(0)
c.take("home-overview", 12, [
    Action(3.8, "frame lower widgets", lambda: c.scroll(900)),
    Action(8.0, "return to overview", lambda: c.scroll(0)),
], park=(306, 40))
```

Motion defaults from the approved demos:

| Operation | Proven setting |
|---|---|
| Visible cursor | `mouse move X Y --duration 650 --steps 40 --human --seed 73` |
| Before click | Settle about 280 ms; then click once |
| Scrolling | `requestAnimationFrame`, 1100 ms, cubic ease-in-out |
| Reading hold | Usually 2–4 seconds after movement settles |
| Editing handles | About 1 second before and after scene action |

The cubic curve is `4*p*p*p` for `p < .5`, otherwise `1 - (-2*p + 2)^3/2`. Apply it to the correct element's `scrollTop`, enforce scroll bounds, and await completion. `--human` applies to pointer motion, not cinematic scrolling. Fixed seeds make pointer curves repeatable, not backend response timing.

Use native `type` for short character-by-character prompts, checking current CLI behavior. Do not invent unsupported delay flags. Budget actual typing duration in a test take; clear an input only when that view-level action is authorized. Submitting an analytical question must produce the real application response.

For chart drilldowns, read actual chart geometry and physically click the real data point. Do not call a hidden callback to fabricate navigation/results. Incidental tooltips may be hidden with a temporary chart display option when authorized, provided data and answers remain intact. Inspect for tooltip flicker before accepting a take.

## Recording and failure handling

Use `record start PATH.mp4 --fps 30 --cursor` on the already-prepared page. Do not pass a URL unless a navigation at recording start is intended. Use separate connector takes for external links: record the actual click, cut cleanly to the authenticated destination, then hold the result. Recheck foreground after tab activation.

Test cursor and scrolling quality before a long run. Run a local fixed driver sequentially with deadlines/readiness timeouts; stop on unexpected state instead of improvising. Keep failed takes separate and out of final media. A recording failure must be corrected by a clean new take, never described as successful.

Do not run TTS, transcription, Cargo builds or substantial FFmpeg encoding concurrently with browser capture: encoder buffering can fail under load. After recording, save key screenshots, verify dimensions/fps, then prepare/render media.

`take()` in the helper writes start/end timing logs and refuses to overwrite existing takes. On failure it attempts to stop recording and marks the log failed. Inspect the error before retrying under a new take name. For a popup transition, use `transition=True` and supply the appropriate used duration later; the helper omits its post-click foreground check, so activate and validate the destination off-take.
