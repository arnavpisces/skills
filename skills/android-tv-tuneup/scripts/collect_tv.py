#!/usr/bin/env python3
"""Collect bounded, read-only ADB diagnostics from an already authorized TV."""
import argparse
import datetime
import json
from pathlib import Path
import re
import subprocess

COMMANDS = [
    ("identity", "date; uptime; am get-current-user; getprop ro.product.model; "
     "getprop ro.product.device; getprop ro.build.display.id; "
     "getprop ro.build.version.release; getprop ro.build.version.security_patch", 20),
    ("packages", "pm list packages -U -f; pm list packages -d", 30),
    ("home", "cmd package resolve-activity --brief -a android.intent.action.MAIN "
     "-c android.intent.category.HOME; dumpsys activity activities", 30),
    ("memory", "cat /proc/meminfo; dumpsys meminfo", 70),
    ("storage", "df -h /data; ls -l /data/system/diskstats_cache.json; dumpsys diskstats", 30),
    ("processes", "ps -A; dumpsys activity services", 40),
    ("cpu", "top -b -n 3 -d 5 -m 12", 30),
]
NETWORK = [
    ("sockets", "ss -tunap; cat /proc/net/tcp; cat /proc/net/tcp6", 25),
    ("netstats", "dumpsys netstats detail", 40),
    ("jobs", "dumpsys jobscheduler; dumpsys alarm", 45),
]


def run(adb, serial, command, timeout):
    start = datetime.datetime.now(datetime.timezone.utc).isoformat()
    try:
        result = subprocess.run([adb, "-s", serial, "shell", command],
                                capture_output=True, text=True, errors="replace",
                                timeout=timeout, check=False)
        return result.stdout + result.stderr, {
            "started_utc": start, "returncode": result.returncode, "timed_out": False}
    except subprocess.TimeoutExpired as error:
        output = error.stdout or b""
        if isinstance(output, bytes):
            output = output.decode("utf-8", errors="replace")
        return output + "\n[Host timeout; output may be incomplete]\n", {
            "started_utc": start, "returncode": None, "timed_out": True}


def summarize(outputs):
    lines = ["Android TV diagnostic summary", "",
             "Raw files may contain private account/device/network information.",
             "CPU samples are not a controlled performance benchmark.",
             "Per-app disk accounting may be cached; check storage.txt timestamp.", ""]
    memory = {k: int(v) for k, v in re.findall(
        r"^(MemTotal|MemAvailable|KReclaimable|SwapTotal|SwapFree):\s+(\d+) kB",
        outputs.get("memory", ""), re.M)}
    total = memory.get("MemTotal", 0)
    if total:
        lines.append(f"Physical RAM reported: {total / 1024:.1f} MiB")
        for key in ("MemAvailable", "KReclaimable"):
            if memory.get(key, 0) > total:
                lines.append(f"WARNING: {key} exceeds physical RAM; disregard this counter.")
    if "SwapTotal" in memory and "SwapFree" in memory:
        used = memory["SwapTotal"] - memory["SwapFree"]
        if 0 <= used <= memory["SwapTotal"]:
            lines.append(f"Logical swapped pages: {used / 1024:.1f} MiB; "
                         "not physical compressed RAM usage.")
    lines += ["", "Cached app storage in MiB (factory system APK sizes may be incomplete):",
              "Package | App | Data | Cache (already included in Data)"]
    arrays = []
    for key in ("Package Names", "App Sizes", "App Data Sizes", "Cache Sizes"):
        match = re.search(r"^" + re.escape(key) + r": (\[.*\])$",
                          outputs.get("storage", ""), re.M)
        try:
            arrays.append(json.loads(match.group(1)) if match else None)
        except (ValueError, TypeError):
            arrays.append(None)
    valid = all(isinstance(a, list) for a in arrays)
    if valid and len({len(a) for a in arrays}) == 1 and all(
            isinstance(v, (int, float)) and v >= 0 for a in arrays[1:] for v in a):
        for package, app, data, cache in sorted(zip(*arrays), key=lambda r: r[1] + r[2], reverse=True):
            lines.append(f"{package} | {app / 1048576:.1f} | {data / 1048576:.1f} | {cache / 1048576:.1f}")
    else:
        lines.append("Unavailable or inconsistent arrays; inspect storage.txt manually.")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--adb", default="adb", help="ADB executable path")
    parser.add_argument("--serial", required=True, help="Authorized and verified TV serial")
    parser.add_argument("--output", required=True, type=Path, help="New local diagnostics directory")
    parser.add_argument("--network", action="store_true", help="Also collect sockets, traffic stats, jobs and alarms")
    args = parser.parse_args()
    try:
        state = subprocess.run([args.adb, "-s", args.serial, "get-state"],
                               capture_output=True, text=True, timeout=15, check=False)
    except (OSError, subprocess.TimeoutExpired) as error:
        parser.exit(1, f"Cannot use ADB: {error}\n")
    if state.returncode or state.stdout.strip() != "device":
        parser.exit(1, "TV is not connected/authorized. Resolve adb devices -l state first.\n")
    try:
        args.output.mkdir(parents=True, exist_ok=False, mode=0o700)
    except OSError as error:
        parser.exit(1, f"Choose a new writable output directory: {error}\n")
    outputs, metadata = {}, {"serial": args.serial, "commands": {}}
    for name, command, timeout in COMMANDS + (NETWORK if args.network else []):
        print(f"Collecting {name}...", flush=True)
        output, info = run(args.adb, args.serial, command, timeout)
        outputs[name] = output
        metadata["commands"][name] = {"command": command, **info}
        (args.output / f"{name}.txt").write_text(output)
    (args.output / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    (args.output / "summary.txt").write_text(summarize(outputs))
    print(f"Saved diagnostics to {args.output.resolve()}", flush=True)
    if any(m["timed_out"] or m["returncode"] != 0 for m in metadata["commands"].values()):
        print("Some commands failed/timed out. Inspect metadata and raw files. "
              "Permission errors can also appear despite a zero shell exit code.")


if __name__ == "__main__":
    main()
