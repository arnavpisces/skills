# Skills

A growing collection of agent skills I've built from tasks that were useful in practice. Each skill captures the workflow, tools, and lessons needed to repeat the task.

## Available skills

| Skill | Description |
| --- | --- |
| [Android TV Tune-up](skills/android-tv-tuneup/SKILL.md) | Discover an Android or Google TV on local Wi-Fi, connect through authorized ADB, inspect CPU, RAM, app storage and background activity, and recommend reversible cleanup. Includes a read-only diagnostic collector and guidance for verifying changes after a reboot. |
| [Create Flowchart](skills/create-flowchart/SKILL.md) | Create reproducible D2 flowcharts with readable source and rendered SVGs, deliberate branching, professional colors, embedded fonts, and visual checks for clipping and routing. Includes a Google Sans variable-font bold helper. |
| [Record Demo](skills/record-demo/SKILL.md) | Create or revise narrated product demos using real browser recordings, natural narration, deliberate cursor and scroll motion, optional animated intros, and verified video exports. Includes a capture runtime, offline tests, and workflow references. |

### Android TV Tune-up

Built from troubleshooting a sluggish OnePlus TV: identifying unused background processes, checking what was actually consuming resources, and verifying changes after a restart.

The skill covers:

- Finding the right TV on the local network and connecting through ADB.
- Inspecting running apps, services, CPU, memory, storage, and optional network activity.
- Separating real resource use from misleading firmware counters and stale storage reports.
- Recommending what to stop, disable, or uninstall, including tradeoffs and rollback.
- Checking the home screen and measuring again after an authorized change.

The diagnostic helper is read-only. Disabling or uninstalling apps is a separate step that follows the user's instructions. The historical package examples are evidence from one TV, not a universal debloat list.

Example prompt:

```text
Use $android-tv-tuneup to find my TV on Wi-Fi, inspect its resource usage,
and recommend what can be disabled or removed. Do the analysis first.
```

Requirements: an Android/Google TV on a reachable local network, Python 3 for the collector, and Android Debug Bridge (ADB). The skill explains how to obtain official platform-tools and handle on-TV authorization. Some diagnostics depend on the TV firmware and available permissions.

### Create Flowchart

Built from creating and refining D2 diagrams: keeping branches auditable, text comfortably inside cards, fonts correctly embedded, and the full flow visible in the rendered output.

The skill covers:

- Writing readable `.d2` source and rendering a matching SVG.
- Choosing sequential, decision, parallel, and retry flows with explicit edge labels.
- Using a consistent professional palette, uppercase box headings, and intentional spacing.
- Embedding the requested fonts and correcting Google Sans variable-font bold rendering.
- Checking the full canvas and natural-size output for missing branches, clipping, overlaps, and excess whitespace.

The default output is the flowchart itself, reading left to right. Surrounding titles and descriptions are added when requested. Keep both the source and rendered output so the diagram can be reproduced.

Example prompt:

```text
Use $create-flowchart to diagram this approval process from left to right.
Show success, rejection, and retry branches, and deliver the D2 source and SVG.
```

Requirements: the D2 CLI (or Go for the documented fallback), an ELK-capable D2 installation for routed branches, and `agent-browser` for visual verification. Custom fonts require their TTF files and licenses. The optional Google Sans bold helper uses Bash, ripgrep (`rg`), and Perl.

### Record Demo

Built from recording and revising narrated product walkthroughs: pairing spoken claims with real UI actions, keeping motion deliberate, and preserving approved footage and narration during focused revisions.

The skill covers:

- Scouting an authenticated application and planning shots against the narration.
- Generating and timing natural narration while preserving unchanged voice files.
- Recording repeatable takes with a visible cursor, eased scrolling, readiness checks, and action allowlists.
- Composing real footage with optional animated intros, continuous zoom, and selective focus.
- Checking the encoded video and audio, then packaging replayable source, clips, and the final script and timing map.

The capture helper supports a scouted, application-specific driver; it does not discover or operate a product automatically. Recording a demo does not authorize consequential production actions. The included Optimus reference describes one local setup and must be adapted and verified before reuse.

Example prompt:

```text
Use $record-demo to create a narrated walkthrough of my app using the supplied
script and my existing authenticated browser session. Capture real UI footage,
add a short animated intro, and deliver the MP4 with replayable source.
```

Requirements: Python 3 for the capture helper, `agent-browser` with a user-authenticated session for the target app, Rust/Cargo with `fframes` for composition, and FFmpeg/ffprobe for media preparation and verification. The `agent-browser` and `fframes-video` skills provide the related tool workflows. Local narration examples use Chatterbox; verify the available runtime, fonts, and voice dependencies before starting.

## Install a skill

For Codex, ask the skill installer to install the individual skill directory:

```text
Use $skill-installer to install android-tv-tuneup from
https://github.com/arnavpisces/skills/tree/main/skills/android-tv-tuneup

Use $skill-installer to install create-flowchart from
https://github.com/arnavpisces/skills/tree/main/skills/create-flowchart

Use $skill-installer to install record-demo from
https://github.com/arnavpisces/skills/tree/main/skills/record-demo
```

Or clone this repository and copy the entire desired skill directory into your agent's skills location. For Codex, that is `$CODEX_HOME/skills`, or `~/.codex/skills` when `CODEX_HOME` is unset. Restart Codex after installing if the skill does not appear immediately.

Keep the complete directory: instructions can depend on its scripts, references, and agent metadata.

## Repository layout

```text
skills/
├── README.md
└── skills/
    ├── android-tv-tuneup/
    │   ├── SKILL.md
    │   ├── agents/
    │   │   └── openai.yaml
    │   ├── references/
    │   │   └── field-guide.md
    │   └── scripts/
    │       └── collect_tv.py
    ├── create-flowchart/
    │   ├── SKILL.md
    │   ├── agents/
    │   │   └── openai.yaml
    │   └── scripts/
    │       └── enable_google_sans_bold.sh
    └── record-demo/
        ├── SKILL.md
        ├── agents/
        │   └── openai.yaml
        ├── references/
        │   ├── capture.md
        │   ├── composition.md
        │   ├── narration.md
        │   ├── optimus-local.md
        │   └── verification.md
        └── scripts/
            ├── capture_runtime.py
            └── test_capture_runtime.py
```

## Adding more skills

Put each new skill in `skills/<skill-name>/` with its own `SKILL.md` and any supporting files it needs. Add its name, link, and description to the table above. Keep generated output, credentials, and device diagnostics out of the repository.
