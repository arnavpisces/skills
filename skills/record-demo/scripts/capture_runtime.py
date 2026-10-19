#!/usr/bin/env python3
"""Session-bound recording helpers; import into a scouted, app-specific driver.

Uses agent-browser's installed CLI. Never launches/closes a browser, logs in,
discovers actions, or overwrites takes. This is a choreography helper, not a
security sandbox. Verify CLI support before use.
"""
from dataclasses import dataclass
from pathlib import Path
from typing import Callable
import json
import math
import re
import shutil
import subprocess
import time


@dataclass(frozen=True)
class Action:
    at: float
    label: str
    run: Callable[[], object]


class Capture:
    def __init__(self, *, session, output, allowed_hosts, allowed_clicks=(),
                 allowed_typing=(), required_state="true", width=1920,
                 height=1080, density=2, fps=30, cli=None):
        if not session or not allowed_hosts:
            raise ValueError("A named session and scouted host allowlist are required")
        if min(width, height, density, fps) <= 0 or fps > 60:
            raise ValueError("Invalid recording dimensions/density/fps")
        self.cli = cli or shutil.which("agent-browser")
        if not self.cli:
            raise RuntimeError("agent-browser unavailable; inspect the installed skill")
        self.session, self.output = session, Path(output).resolve()
        self.hosts, self.clicks = set(allowed_hosts), set(allowed_clicks)
        self.typing, self.required_state = set(allowed_typing), required_state
        self.width, self.height, self.density, self.fps = width, height, density, fps
        for folder in ("clips", "screenshots", "review"):
            (self.output / folder).mkdir(parents=True, exist_ok=True)

    def call(self, *args, js=None, timeout=12, pin=True):
        command = [self.cli, "--session", self.session]
        if pin:
            command.append("--pin-tab")
        result = subprocess.run(command + ["--json", *map(str, args)],
                                input=js, text=True, capture_output=True,
                                timeout=timeout, check=False)
        if result.returncode:
            raise RuntimeError(f"agent-browser {args[0]} failed (exit {result.returncode})")
        try:
            data = json.loads(result.stdout)
        except json.JSONDecodeError as error:
            raise RuntimeError("Unexpected CLI output; check installed JSON schema") from error
        if not data.get("success"):
            raise RuntimeError(f"agent-browser {args[0]} rejected the operation")
        return data.get("data", {})

    def ev(self, js):
        return self.call("eval", "--stdin", js=js)["result"]

    def check(self):
        return self.ev(f"""(()=>{{
          if(innerWidth!=={self.width}||innerHeight!=={self.height}||devicePixelRatio!=={self.density})
            throw Error('Viewport changed');
          if(document.hidden)throw Error('Lost foreground');
          if(!{json.dumps(sorted(self.hosts))}.includes(location.hostname))
            throw Error('Unexpected host or authentication needed');
          if(!({self.required_state}))throw Error('Required appearance/state absent');
          return true;
        }})()""")

    def ready(self, condition, timeout=20):
        end = time.monotonic() + timeout
        while time.monotonic() < end:
            self.check()
            if self.ev(condition) is True:
                return
            time.sleep(.25)
        raise RuntimeError("Readiness timed out; stop and scout again")

    def activate(self, tab):
        self.call("tab", tab, pin=False)
        self.call("set", "viewport", self.width, self.height, self.density)
        self.check()

    def move(self, x, y, seed=73, ms=650, steps=40):
        self.check()
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise ValueError("Pointer destination outside viewport")
        self.call("mouse", "move", round(x), round(y), "--duration", ms,
                  "--steps", steps, "--human", "--seed", seed)

    def click(self, selector, *, popup=False):
        if selector not in self.clicks:
            raise RuntimeError("Click outside the scouted action allowlist")
        self.check()
        point = self.ev(f"""(()=>{{
          const es=document.querySelectorAll({json.dumps(selector)});
          if(es.length!==1)throw Error('Click target missing or ambiguous');
          const e=es[0],r=e.getBoundingClientRect();
          if(r.width<1||r.height<1||r.left<0||r.right>{self.width}||r.top<0||r.bottom>{self.height})
            throw Error('Click target not framed');
          if(e.disabled)throw Error('Click target disabled');
          const x=r.x+r.width/2,y=r.y+r.height/2,hit=document.elementFromPoint(x,y);
          if(!hit||!(hit===e||e.contains(hit)))throw Error('Click target obscured');
          return {{x,y}};
        }})()""")
        self.move(point["x"], point["y"], seed=41)
        time.sleep(.28)
        self.call("click", selector)
        if not popup:
            self.check()

    def type(self, selector, text):
        if selector not in self.typing:
            raise RuntimeError("Typing outside the scouted input allowlist")
        self.check()
        self.call("type", selector, text)
        self.check()

    def scroll(self, target, container=None, ms=1100):
        self.check()
        if not math.isfinite(target) or ms <= 0:
            raise ValueError("Invalid scroll target/duration")
        element = "document.scrollingElement" if container is None else (
            f"document.querySelector({json.dumps(container)})")
        return self.ev(f"""(async()=>{{
          const e={element};if(!e)throw Error('Scroll container absent');
          const target={target};if(target<0||target>e.scrollHeight-e.clientHeight+2)
            throw Error('Scroll outside container');
          const from=e.scrollTop;
          await new Promise((resolve,reject)=>{{
            let t0;function step(t){{
              if(document.hidden){{reject(Error('Lost foreground'));return}}
              t0??=t;const p=Math.min(1,(t-t0)/{ms});
              const q=p<.5?4*p*p*p:1-Math.pow(-2*p+2,3)/2;
              e.scrollTop=from+(target-from)*q;
              if(p<1)requestAnimationFrame(step);else resolve();
            }}requestAnimationFrame(step);
          }});
          if(Math.abs(e.scrollTop-target)>2)throw Error('Scroll failed');
          return e.scrollTop;
        }})()""")

    def screenshot(self, name):
        if not re.fullmatch(r"[A-Za-z0-9_-]+", name):
            raise ValueError("Unsafe screenshot name")
        self.call("screenshot", self.output / "screenshots" / f"{name}.png")

    def _verify_clip(self, path, minimum_seconds):
        result = subprocess.run([
            "ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
            "stream=width,height,r_frame_rate:format=duration", "-of", "json", str(path)
        ], capture_output=True, text=True, timeout=30, check=True)
        probe = json.loads(result.stdout)
        video = probe["streams"][0]
        expected = (round(self.width*self.density), round(self.height*self.density), f"{self.fps}/1")
        if (video["width"], video["height"], video["r_frame_rate"]) != expected:
            raise RuntimeError("Recording is not the promised native resolution/fps")
        if float(probe["format"]["duration"]) < minimum_seconds - .3:
            raise RuntimeError("Take truncated; inspect recording before reuse")
        return probe

    def take(self, name, seconds, actions, *, park, lead=1., tail=1.,
             transition=False, late_tolerance=.55):
        if not re.fullmatch(r"[A-Za-z0-9_-]+", name):
            raise ValueError("Unsafe take name")
        if not math.isfinite(seconds) or seconds <= 0 or min(lead, tail, late_tolerance) < 0:
            raise ValueError("Invalid take duration/handles")
        actions = list(actions)
        times = [a.at for a in actions]
        if times != sorted(times) or any(not math.isfinite(t) or t < 0 or t >= seconds for t in times):
            raise ValueError("Actions must be ordered and inside the scene duration")
        path = self.output / "clips" / f"{name}.mp4"
        log_path = self.output / "review" / f"{name}-capture.json"
        if path.exists() or log_path.exists():
            raise RuntimeError("Existing take preserved; choose a fresh name/destination")
        self.check()
        self.move(*park, seed=12)
        self.screenshot(name + "-before")
        log = dict(clip=path.name, status="failed", seconds=seconds, trim_lead=lead,
                   tail_handle=0 if transition else tail, actions=[],
                   css_viewport=[self.width, self.height], device_scale_factor=self.density,
                   resolution=[round(self.width*self.density), round(self.height*self.density)], fps=self.fps)
        error = None
        started = False
        try:
            self.call("record", "start", path, "--fps", self.fps, "--cursor")
            started = True
            time.sleep(lead)
            start = time.monotonic()
            for action in actions:
                elapsed = time.monotonic() - start
                if elapsed > action.at + late_tolerance:
                    raise RuntimeError("Choreography late: " + action.label)
                time.sleep(max(0, action.at - elapsed))
                began = time.monotonic() - start
                action.run()
                ended = time.monotonic() - start
                log["actions"].append(dict(action=action.label, start=round(began, 3), end=round(ended, 3)))
                if ended > seconds + late_tolerance:
                    raise RuntimeError("Action exceeds scene budget: " + action.label)
            if not transition:
                time.sleep(max(0, seconds + tail - (time.monotonic() - start)))
                self.check()
        except Exception as failure:
            error = failure
        finally:
            if started:
                try:
                    self.call("record", "stop", timeout=30)
                except Exception as failure:
                    log["stop_error"] = str(failure)
                    if error is None:
                        error = failure
        try:
            if error is not None:
                raise error
            log["probe"] = self._verify_clip(path, 0 if transition else seconds + lead + tail)
            if not transition:
                self.screenshot(name + "-after")
            log["status"] = "passed"
        except Exception as failure:
            log["error"] = str(failure)
            raise
        finally:
            log_path.write_text(json.dumps(log, indent=2) + "\n")
        return log
