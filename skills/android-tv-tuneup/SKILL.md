---
name: android-tv-tuneup
description: Discover Android or Google TVs on local Wi-Fi, connect through authorized ADB, inspect CPU, RAM, app storage and background activity, and recommend reversible cleanup. Use for slow smart TVs, unused launchers or assistants, and post-reboot checks; not for non-Android TVs or repository performance work.
---

# Android TV Tune-up

Diagnose the user's TV from measurements, then recommend changes with clear benefits, functional losses and rollback commands. Read [the field guide](references/field-guide.md) for discovery, ADB setup, commands and firmware measurement pitfalls from a OnePlus TV investigation.

## Debugging setup helper

Before the first ADB connection attempt, establish whether debugging is enabled. If a current authorized ADB connection already works or the user has just confirmed setup, continue without asking again. Otherwise use [the debugging setup helper](references/debugging-setup.md) to ask whether USB debugging or wireless/network debugging is enabled in Developer options, then guide the user according to their answer. Local-network discovery and checking host tools can proceed while waiting; do not repeatedly attempt ADB connections before setup is resolved.

## Discover and identify

- Identify the host's active LAN interface and subnet. Prefer mDNS Android TV remote and Google Cast advertisements; resolve targets to current addresses. DHCP addresses change. Cross-check model/device identity after connecting; an old IP or Cast name alone is insufficient.
- Keep discovery scoped to the user's network and intended device. If multiple TVs match, ask which one. If discovery fails, ask for the TV's network-settings address when necessary; lack of mDNS is not proof the TV is offline.
- Reuse available ADB. Otherwise download Google's official platform-tools for the host OS outside the project. Do not root the TV or bypass device authorization.
- Connect to an observed ADB endpoint. An open port proves reachability, not authentication. For unauthorized/offline devices explain the on-TV debugging or pairing step. Stop retrying until the relevant state changes. Keep pairing codes and credentials out of reports.

## Inspect before recommending

Run `scripts/collect_tv.py --adb PATH --serial SERIAL --output NEW_DIRECTORY` after connection and identity verification. The helper collects read-only diagnostics with bounded per-command timeouts, saves raw evidence and a caveated summary, and never installs, stops, disables, clears or uninstalls apps. Add `--network` only for a relevant background/network investigation. Each run requires a new output directory. Collection can take a few minutes; communicate progress while it runs. Read relevant saved files rather than dumping everything into chat.

- Capture uptime, build/security patch, RAM, live disk usage, package/UID inventory, processes/services, interval CPU samples and app memory. Check default HOME before discussing launchers.
- Compare proportional memory (PSS) and label RSS separately. Virtual address space is not RAM use. Storage cleanup and RAM savings are different outcomes. Cached processes need not be performance problems.
- Let boot activity settle and resample. Compare equivalent screens, workloads and uptime windows. State confounders; don't claim causality from short samples.
- Check Android diskstats cache's timestamp. Data includes cache: don't add it twice. Factory system APKs may be accounted differently from downloaded updates, and user-scoped removal may reclaim little disk space. Label unreadable data and partial `du` totals as incomplete.
- For telemetry questions, distinguish encrypted sockets, scheduled analytics jobs and actual transfers. Shared system UIDs prevent package-level attribution. Stale traffic counters don't prove inactivity. A retained job entry isn't proof it can run; inspect readiness/component state.

## Recommend and, when authorized, change

Rank candidates by measured cost, household usage, reversibility and lost features. Identify exact packages and confidence; words such as "analytics", "assistant" or "recommendations" in a name are not sufficient evidence. Separate user apps from vendor/system components.

Inspection or recommendations alone don't authorize app changes. When the user explicitly chooses a change, proceed within that scope without asking again. Broader cleanup requests may authorize routine changes, but don't silently delete logins/downloads, replace the home experience or disable core functionality. The historical OnePlus example is not standing consent for another session.

- Prefer temporary force-stop for an experiment and `pm disable-user --user USER PACKAGE` for an agreed persistent disable. Verify Android's current user. Record original enabled state for exact rollback (`pm default-state`, `pm enable`, etc.).
- Before disabling a launcher, verify a working enabled HOME alternative and its default resolution. Test Home navigation and settings access afterward. Never disable both launchers.
- Don't broadly disable Play services, System UI, Settings, package installation, DRM, media/TV input, network, Bluetooth/remote or firmware components to chase RAM. Assess explicitly requested system-component changes individually.
- Clearing data loses account/settings state; uninstalling may remove downloads and data. Explain consequences when not already authorized. `install-existing` cannot recover deleted app data.
- Disabling recommendations doesn't establish that ads or Discover/Shop disappear. DNS filtering requires validated domains and may cause retries or breakage. Launcher replacement is a separate user decision.

## Verify and report

After changes verify package state, processes/services, default HOME and interval CPU/memory. Inspect the actual home screen when requested, using XML or screenshots. Keep app data intact unless deletion was authorized.

For a requested reboot check, verify changed uptime and repeat measurements; don't reboot the TV unprompted. Report persistence, caveated before/after measurements with units and conditions, functional effects and rollback. Save evidence outside the repository, keep account/network identifiers private, and identify created files for eventual cleanup.
