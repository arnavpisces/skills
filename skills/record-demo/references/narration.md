# Natural narration and timing

The script is the spoken source; editor directions belong in shot metadata. Preserve exact user text unless rewriting/shortening is requested. Derive timing from measured generated voice, not estimated word counts or an arbitrary scene length.

## Local Chatterbox workflow

Inspect the installed narration runtime and Python environment first. On the local Optimus machine, `chatterbox-tts/tts_runtime.py` exposes `load_model`, `generate_narration`, `load_pronunciations` and `inspect_wav`; its `.venv/bin/python` contains Torch and audio dependencies. A persistent generation process can load the model once and generate paragraphs sequentially; wait for its actual exit status and outputs.

The accepted later intro/live-demo voice is Chatterbox **Original**, MPS, English, no cloned reference:

```python
model = load_model('original', 'mps')
torch.manual_seed(73)
result = generate_narration(
    model, text, model_name='original', device='mps', reference=None,
    exaggeration=.5, cfg_weight=.5, pause_ms=220,
    pronunciations=pronunciations, output_path=raw_wav,
    max_sentences=3, temperature=.65,
)
assert inspect_wav(result.wav)['ok']
```

Verify these APIs before reuse; another environment may need a supported device/runtime. The earlier executive pitch used different parameters, so prefer the **approved current scene's settings**, not an older note. Keep seeds and parameters in project metadata. Seed controls alone do not guarantee cross-device/model bit-identical output.

Use the local pronunciation dictionary for product names/acronyms. Do not edit a global pronunciation dictionary for one clip without that scope; apply project-specific overrides locally when needed. Voice cloning requires user authorization and an appropriate reference; do not introduce it for this workflow by default.

## Processing and pacing

Generate new/changed paragraphs separately and retain unchanged WAVs. Track script/parameter fingerprints so a stale cached raw WAV cannot be silently reused after its script changes. Treat a preexisting raw file as reusable only when its provenance matches; otherwise create a new filename.

Validate WAV sample rate, channel count, duration, non-silence and clipping. Trim only leading/trailing silence, keeping short breathing room (the accepted workflow retained roughly 70 ms lead / 120 ms tail). Do not remove internal dramatic pauses or alter time scale. Detect an all-silent result before trimming.

Normalize source narration conservatively; the accepted source setting was:

```sh
ffmpeg -y -i trimmed.wav -af loudnorm=I=-16:TP=-2:LRA=7 -ar 48000 voice.wav
```

Use explicit input/output files; never overwrite approved voice. Rendered audio loudness depends on voice gain, score, ducking and master gain, so inspect the composition mix and exported AAC again.

For the live demo, a useful measured scene budget was voice duration + 1.6 seconds, rounded **up** to the next 30 fps frame, with voice starting 0.6 seconds into the scene. Adjust for actual clicks/reading holds. A narration that ends before the last important result has been read needs a longer visual hold, not hurried choreography.

When duration is too long, shorten redundant narration within the user's editing authorization. Maintain the natural voice settings and content intent. Do not use `atempo`, pitch shifts, overly tight sentence segmentation or reduced pauses just to meet a target. `max_sentences=1` can sound fragmented and accumulate unnatural pauses; the proven setting is 3. Exact-script requests that cannot fit the desired duration require explaining the conflict before making unauthorized cuts.

## Speech verification

Check pronunciation and naturalness using a representative audio preview, then verify revised paragraphs against the final script. ASR/transcription can catch skipped/repeated phrases, but cannot establish that a voice sounds natural. Distinguish ASR punctuation/inflection differences from actual omissions. Keep transcription provenance for reused approved audio.

Do not run transcription during browser takes. In this local setup, the Whisper environment contains Whisper but lacks Torch; the Chatterbox environment contains Torch. The working combination is Chatterbox Python with the Whisper site-packages on `PYTHONPATH`, a cached `small.en` model, CPU and 4 Torch threads. Recheck environment availability before using this workaround; do not install duplicate runtimes merely because the wrong interpreter was selected.

Record paragraph IDs, exact narration, voice file, voice duration, global voice start, scene start/end/frame count and all voice-generation parameters in the project manifest.
