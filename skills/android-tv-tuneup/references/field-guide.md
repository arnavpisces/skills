# Field guide

## Discovery and connection

On macOS use `route -n get default`, `ifconfig INTERFACE`, and `arp -an`. On Linux use `ip route`, `ip addr`, and `ip neigh`. Don't assume en0 or a subnet.

macOS mDNS examples (long-running: stop after collecting results):

```sh
dns-sd -B _androidtvremote2._tcp local.
dns-sd -B _googlecast._tcp local.
dns-sd -L 'OBSERVED SERVICE NAME' _androidtvremote2._tcp local.
dns-sd -G v4 OBSERVED-TARGET.local.
```

Linux alternatives include `avahi-browse -rt _androidtvremote2._tcp` or `_googlecast._tcp`. A remote service on 6466 or Cast on 8009 doesn't grant ADB access. Legacy network ADB commonly uses 5555; newer Android wireless debugging has separate pairing and connection ports. Use observed or TV-displayed endpoints rather than guessing a pairing port. Don't enable legacy network debugging unless the user has requested it and understands the local-network exposure.

Find ADB with `command -v adb` or the Android SDK platform-tools directory. Official downloads if needed:

- macOS: https://dl.google.com/android/repository/platform-tools-latest-darwin.zip
- Linux: https://dl.google.com/android/repository/platform-tools-latest-linux.zip
- Windows: https://dl.google.com/android/repository/platform-tools-latest-windows.zip

Extract into a dedicated tools/temp directory outside the project. Retain existing ADB keys. Then:

```sh
adb connect ADDRESS:PORT
adb devices -l
adb -s SERIAL shell 'getprop ro.product.model; getprop ro.product.device; getprop ro.serialno; am get-current-user'
```

The user must approve debugging on-screen if prompted. For wireless pairing use `adb pair TV-DISPLAYED-PAIRING-ENDPOINT` with an interactive code, then connect to the distinct connection endpoint. Don't weaken authorization.

One observed host failure: an old ADB daemon reported "No route to host" while new TCP sockets to the TV worked. Restarting that daemon fixed it. `adb kill-server` affects all ADB sessions: consider active work before using it. Diagnose genuine routing/address failures separately.

## Read-only inspection

Use the selected serial consistently. These commands differ by firmware; permission denial is an evidence limit, not a reason to root.

```sh
adb -s SERIAL shell 'date; uptime; am get-current-user'
adb -s SERIAL shell 'getprop ro.build.display.id; getprop ro.build.version.release; getprop ro.build.version.security_patch'
adb -s SERIAL shell cat /proc/meminfo
adb -s SERIAL shell df -h /data
adb -s SERIAL shell top -b -n 3 -d 5 -m 12
adb -s SERIAL shell pm list packages -U -f
adb -s SERIAL shell ps -A
adb -s SERIAL shell dumpsys meminfo
adb -s SERIAL shell dumpsys meminfo PACKAGE
adb -s SERIAL shell dumpsys diskstats
adb -s SERIAL shell ls -l /data/system/diskstats_cache.json
adb -s SERIAL shell cmd package resolve-activity --brief -a android.intent.action.MAIN -c android.intent.category.HOME
adb -s SERIAL shell dumpsys package PACKAGE
adb -s SERIAL shell dumpsys activity services PACKAGE
```

For network/background questions: `ss -tunap`, `/proc/net/tcp`, `/proc/net/tcp6`, `dumpsys netstats detail`, `dumpsys jobscheduler`, `dumpsys alarm`. Avoid collecting account settings or all logs by default. Restrict log inspection to the question and redact identifiers before sharing.

For screenshots, vendor binaries may print diagnostic text into `exec-out screencap -p` and corrupt the PNG. Prefer saving on-device and pulling:

```sh
adb -s SERIAL shell screencap -p /sdcard/TASK-screen.png
adb -s SERIAL pull /sdcard/TASK-screen.png /ABSOLUTE/OUTPUT/screen.png
adb -s SERIAL shell uiautomator dump /sdcard/TASK-ui.xml
adb -s SERIAL pull /sdcard/TASK-ui.xml /ABSOLUTE/OUTPUT/ui.xml
```

Use task-specific filenames. These create diagnostic files, not settings changes. Remove only task-owned captures when no longer needed. UI dump can fail to reach idle while the launcher animates; use screenshots. Inspect the image before asserting results. Quote deep-link URLs containing `?` to avoid host-shell globbing.

## Measurement pitfalls

- Four-core `top` may report 400% capacity. Device-wide busy proportion is `(capacity - idle) / capacity`; process percentages are relative to one core. First samples can be noisy. High load plus idle CPU may indicate blocked tasks rather than CPU saturation.
- OnePlus C00 firmware reported impossible `MemAvailable` and `KReclaimable`, affecting dumpsys aggregate free RAM too. Check plausibility against physical RAM. `top` sometimes misformatted memory counters; cross-check raw `/proc/meminfo`.
- zRAM keeps compressed swapped pages in RAM. `SwapTotal - SwapFree` measures logical swapped pages, not physical zRAM cost. Existing swap doesn't prove active thrashing. Look for repeated reclaim/swapping and interaction symptoms.
- RSS includes shared pages: don't sum across apps. Prefer PSS; graphics memory changes as screens load.
- Diskstats emits aligned JSON arrays: `Package Names`, `App Sizes`, `App Data Sizes`, `Cache Sizes`. Data includes cache. Cache timestamps may predate installations; system APK totals can be incomplete. `du` with permission errors is a lower bound.
- DHCP, DNS, mDNS, SSDP, Cast and remote sockets aren't inherently telemetry. TLS hides payloads. UID 1000 is shared by many system packages. Don't infer vendors from IP guesses or claim that established connections mean continuous uploads.

## Mutations and rollback

Only after user authorization; substitute verified current user and exact package:

```sh
adb -s SERIAL shell am force-stop PACKAGE
adb -s SERIAL shell pm disable-user --user USER PACKAGE
adb -s SERIAL shell pm list packages -d
adb -s SERIAL shell pidof PACKAGE
adb -s SERIAL shell dumpsys activity services PACKAGE
```

Record original enabled state. For initial `enabled=0` (default), restore using `pm default-state --user USER PACKAGE`. For explicitly enabled packages use `pm enable --user USER PACKAGE`. Check `pm help` if an option isn't supported. Force-stopped state differs from enabled state; launch only when appropriate to requested rollback.

`pm uninstall --user USER PACKAGE` can delete user data without reclaiming the system APK. `cmd package install-existing --user USER PACKAGE` can re-register an existing system package, not recover deleted settings/downloads. Removed user APKs may need official-source reinstallation. Prefer disabling for trials.

## Historical OnePlus example — not defaults

A OnePlus C00 / Android 11 household explicitly requested disabling these packages, then verified persistence after reboots:

- `com.google.android.katniss`: unused Assistant interactor repeatedly used 25–30% of one CPU core. Disabling stopped voice/search processes.
- `com.oneplus.tv.launcher`: unused alongside verified default `com.google.android.tvlauncher`.
- `com.google.android.tvrecommendations`: ~25 MiB PSS background process. Disabling stopped it, but sponsored banners, Discover, Shop and recommendation rows remained.

No Play services, media, network, TV input, HeyTap push or firmware components were disabled. Storage had ~5.1 GiB free, so disk cleanup was a lower priority. Later CPU/swap snapshots improved but weren't controlled benchmarks. Never hard-code that device's old IP, package choices, preferences or consent into another session.
