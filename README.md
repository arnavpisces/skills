# Skills

A growing collection of agent skills I've built from tasks that were useful in practice. Each skill captures the workflow, tools, and lessons needed to repeat the task.

## Available skills

| Skill | Description |
| --- | --- |
| [Android TV Tune-up](skills/android-tv-tuneup/SKILL.md) | Discover an Android or Google TV on local Wi-Fi, connect through authorized ADB, inspect CPU, RAM, app storage and background activity, and recommend reversible cleanup. Includes a read-only diagnostic collector and guidance for verifying changes after a reboot. |

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

## Install a skill

For Codex, ask the skill installer to install the individual skill directory:

```text
Use $skill-installer to install android-tv-tuneup from
https://github.com/arnavpisces/skills/tree/main/skills/android-tv-tuneup
```

Or clone this repository and copy the entire desired skill directory into your agent's skills location. For Codex, that is `$CODEX_HOME/skills`, or `~/.codex/skills` when `CODEX_HOME` is unset. Restart Codex after installing if the skill does not appear immediately.

Keep the complete directory: instructions can depend on its scripts, references, and agent metadata.

## Repository layout

```text
skills/
├── README.md
└── skills/
    └── android-tv-tuneup/
        ├── SKILL.md
        ├── agents/
        │   └── openai.yaml
        ├── references/
        │   └── field-guide.md
        └── scripts/
            └── collect_tv.py
```

## Adding more skills

Put each new skill in `skills/<skill-name>/` with its own `SKILL.md` and any supporting files it needs. Add its name, link, and description to the table above. Keep generated output, credentials, and device diagnostics out of the repository.
