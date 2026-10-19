# Animated intros and real-footage composition

## Establish the project

Read the installed `fframes-video` design/API/audio references when available. Verify `cargo-fframes --help`, Cargo dependencies and the generated CLI; use the installed release and supported backend. The approved local demo uses fframes **1.1.0**, Skia Metal on macOS, Rust/SVG scenes and H.264/AAC. This is a proven example, not a mandatory version pin for all future projects.

Work in a standalone Cargo project. Build and run inspect/render commands there, not in the application's repo root. Preserve existing dirty/untracked app work. Use a shared external Cargo target cache when helpful without packaging it.

For an intro-only request, create only the intro. For a first cut through Home, stop there. For revisions, create a separate project/output name and retain unaffected scene media and voice. Rebuild timing from measured audio; never reuse old global timestamps after shortening paragraphs.

## Intro storytelling

Reuse an approved layout and identity when the user likes them. A useful three-beat executive intro is **problem → operational challenge → product approach**. Make each scene communicate one idea; let concise headlines and restrained motion support the voice rather than duplicate every sentence.

The Optimus reference uses:

- Cream `#F2F0E9`, dark teal `#123C3B`, mint `#BAE5C8`, orange `#E98450`, supporting teal `#23736B`.
- DM Sans, spacious two-line headlines, a restrained top brand strip, eased 300–650 ms entrances and staggered workflow nodes/cards.
- Full brand line: `OPTIMUS AI - AUTONOMOUS SECURITY CENTER OF EXCELLENCE`.
- Discovery → understanding → approval → execution → verification, grounded in actual governance/execution boundaries.

Use these only for this established identity; other products inherit their own brand. Do not invent autonomy, impact statistics or capabilities to fill the motion design. Measure text with actual fonts; inspect settled frames for headline and brand-line fit. Keep adequate holds around scene transitions.

For a fixed 20-second intro, budget words against a natural-speed sample before designing the timeline. If the approved text does not fit and brevity is authorized, remove redundant sentences while preserving the key message. Do not repeat the failed approach of squeezing long narration into the target through speed-up.

## Real footage and media providers

Inspect the actual version's media APIs before coding. In the proven 1.1.0 project:

- Fonts are compiled via `include_media_dir!`.
- MP4s, WAVs and score load through `MediaDirectory::read_folder()` and `process_media_source()`.
- `CombinedMediaProvider` combines embedded fonts with runtime media; using embedded assets alone can omit the external score/footage.
- `FFramesSyncedVideoFrame` with `SyncVideoFrameInput::default()` supplies the actual decoded clip frame; use `Svgr::empty()` when unavailable and make missing media an inspection failure before delivery.
- Scene voice uses `AudioTrack::new(..., Second(0.6)..Eof).voice()`; the 0.6-second lead is an example based on handles, not universal.
- Music uses conservative gain, fades and `duck_under_voice()`. Validate the final mix rather than copying one gain setting blindly.

Native 4K rendering can use an SVG `viewBox="0 0 1920 1080"` with output width/height 3840×2160; source recordings must already be native 4K. Align `Video` dimensions and renderer surface dimensions. For intros, vector scenes scale cleanly; for UI footage, limit digital enlargement and inspect at full size.

Trim only handles and unwanted waiting, maintaining playback speed. The proven source-media H.264 CRF 12 / final CRF 14 preserves interface text; it is a starting point, not a guarantee. Minimize lossy encoding generations. Keep roughly 0.2 seconds of source media beyond each scene's requested length for decoder EOF safety; otherwise inspect the last few frames for blank/missing video. Connector edits must deliberately remove unused tails rather than accidentally including them twice.

## Camera and focus

Map editorial coordinates into footage coordinates. For zoom `scale = 1 + z` about anchor `(cx, cy)`, translate by `(-cx*z, -cy*z)` before scaling. Clip to the video frame. Keeping the same anchor/scale at adjoining scene boundaries avoids a snap.

For retained homepage zoom, ease to 110% once and retain that scale while the recorded scrolling moves through widgets. Do not bake separate artificial scrolls into the reconstructed interface.

Green focus treatment: compute the target rectangle under the same camera transform; draw a full-frame path with an even-odd hole. Tint outside it with dark teal at about 0.48 opacity and use a subtle green border. Fade it in/out over roughly 0.8 seconds. The real target UI stays clear. Full-widget focus and selective KPI focus are different rectangles; choose the one the editor requested.

Avoid simultaneous scrolling, zooming and highlight changes unless the motion clearly supports one idea. Let a reading hold follow each action. Keep labels short and away from essential UI. End a focus before scrolling away from its target, unless the mask itself tracks that target intentionally.

When narration changes but a scene's action remains valid, shorten the scene's end and adjust its camera/focus hold durations; do not silently accelerate footage or reuse a too-short source. When the user changes theme or actual interaction, recapture affected scenes.

## Revision provenance

Record which scenes were newly captured, reused, re-trimmed or had only narration changed. Preserve approved raw clips; reuse integrated MP4/voice files byte-for-byte when unchanged. Verify hashes for important preserved sections and for an intro whose preservation matters. Update the manifest and the full narration/screen-actions document to the final timeline.
