# Verification and delivery

Run tools in the generated fframes Cargo project. Inspect installed CLI help; time/scene selectors differ across releases. In the proven 1.1.0 CLI, scene indices are **zero-based** (`#0` is the first scene), and repeated scene types make absolute timestamps or manifest IDs safer for QA.

```sh
cargo build --release --bin YOUR_BINARY
./target/release/YOUR_BINARY timeline --json
./target/release/YOUR_BINARY inspect --all-frames --fail-on warning --json
./target/release/YOUR_BINARY strip all -n 24 -o review/storyboard.png
./target/release/YOUR_BINARY frame 1.2s 6.5s -o review/detail
./target/release/YOUR_BINARY audio analyze --json
./target/release/YOUR_BINARY render -o demo.mp4
```

Use focused range/draft renders before expensive full renders when a scene is uncertain. Run relevant generated project tests when they exist; a newly created snapshot baseline needs visual review before acceptance. Do not invent tests that merely repeat source code. Fix composition findings and clearly separate upstream toolchain warnings from missed checks.

Open the actual PNGs/contact sheets. Review:

- Intro headline/brand fit, scene reading time and natural voice alignment.
- Beginning/end of each take, links/clicks, scroll transitions, retained zoom boundaries and focus masks.
- Native-size UI text and important counts/statuses; captions must not cover them.
- Last few frames of scenes for decoder EOF blanks or tail flashes.
- Waiting edits and processing labels; real response provenance and action/status distinctions.

Inspect the **encoded** export as well, not just composition PNGs. Extract a contact sheet spanning every scene and native-size frames at important result states. Check motion with a strip concentrated around scrolling/clicking; endpoints alone do not establish smooth motion. Offer the video/preview for human playback, while reporting the agent's actual review method accurately.

## Final media checks

```sh
ffprobe -v error -show_entries \
  format=duration,size:stream=codec_name,width,height,r_frame_rate,nb_frames,sample_rate,channels \
  -of json demo.mp4
ffmpeg -v error -i demo.mp4 -map 0:v:0 -f null -
ffmpeg -hide_banner -i demo.mp4 -vn -af ebur128=peak=true -f null -
```

Require the promised actual resolution, frame rate, duration and frame count, matching the manifest. Check full video decode for corruption. Aim for roughly -14 to -16 LUFS, true peak at or below -1 dBTP, and no clipped samples unless the user specifies another delivery standard. Encoded AAC may peak differently from source WAV; validate it separately. If the delivery exceeds the intended peak, adjust gain/limiting and recheck rather than quoting source-audio results.

## Deliverables

Use the requested part/revision name and preserve previous approved files. A complete demo delivery normally includes:

- Final MP4, inline preview or local link.
- Standalone source composition, Cargo.toml/lock, runtime media/font assets.
- Project-specific capture/replay driver and copied runtime helper.
- Individual clean MP4 takes with handles and screenshots of key states.
- Final script paired with screen actions and actual timings.
- Shot manifest: dimensions, CSS viewport/density/fps, narration/voice timings, clip trim/used durations, timed actions, scroll containers, focus/zoom and source/reuse provenance.
- Voice generation settings and normalized audio, score source if authored, and concise verification evidence.

Package a curated source bundle. Exclude browser profiles, state/cookies/tokens, unrelated repositories/configs, build targets, failed takes, transient decoder/encode pieces, Python caches and unnecessary review intermediates. Do not automatically archive an entire working directory. Generate a checksum manifest and verify the ZIP CRC and expected file inventory. Confirm the extracted source can locate its packaged assets without depending on a live login.

Summarize what changed, final duration/resolution, and any material unverified limitation. Use the full current script/screen-action map for further editorial feedback. A safe production demo displays existing consequential records; approval/dispatch flows should not be enacted merely for a recording.
