import json
from datetime import datetime
from pathlib import Path
from .paths import STATE_DIR, STATE_FILE, DEBUG_LOG, OPT_CONFIG, OPT_DIR

DEFAULT_CONFIG = {
    "app_name": "neandertimeline_modular",
    "free_online_ai_ok": False,
    "google_ai_key_env": "GOOGLE_API_KEY",
    "fallback_ai_key_envs": ["GEMINI_API_KEY", "FREE_ONLINE_AI_API_KEY"],
    "autosave": True,
    "mp4_allowed_only_by_button": True,
    "safe_ai_patch_mode": True,
    "reject_destructive_ai_patches": True
}

def ensure_dirs():
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    try:
        OPT_DIR.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        pass

def read_json(path, default):
    p = Path(path)
    if not p.exists():
        return default
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return default

def write_json(path, data):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False, default=str), encoding="utf-8")

def load_config():
    ensure_dirs()
    cfg = dict(DEFAULT_CONFIG)
    if OPT_CONFIG.exists():
        cfg.update(read_json(OPT_CONFIG, {}))
    return cfg

def save_config(cfg):
    ensure_dirs()
    write_json(OPT_CONFIG, cfg)

def load_state(default_state):
    ensure_dirs()
    if STATE_FILE.exists():
        state = read_json(STATE_FILE, default_state)
        if not isinstance(state, dict) or "scenes" not in state or not isinstance(state.get("scenes"), list):
            bad = STATE_FILE.with_name("living_timeline_state.rejected_or_broken.json")
            try:
                STATE_FILE.rename(bad)
            except Exception:
                pass
            write_json(STATE_FILE, default_state)
            return default_state
        for k, v in default_state.items():
            state.setdefault(k, v)
        return state
    write_json(STATE_FILE, default_state)
    return default_state

def save_state(state):
    write_json(STATE_FILE, state)

def log(message):
    ensure_dirs()
    line = f"[{datetime.now().isoformat(timespec='seconds')}] {message}"
    old = DEBUG_LOG.read_text(encoding="utf-8") if DEBUG_LOG.exists() else ""
    DEBUG_LOG.write_text(old + line + "\n", encoding="utf-8")

def patch_request_text(error_text=""):
    return f"""Google AI, the following error occurred.

{error_text}

Please provide a command I can paste into terminal that will fix this error.

Important safeguard:
Do not replace /opt/neandertimeline_modular/neandertimeline_app.py with a smaller app.
Do not remove the map canvas.
Do not remove Back, Play, Next, AI Improve, Apply AI Patch, Export, or Make MP4.
Do not overwrite living_timeline_state.json unless the patch contains a valid scenes list with map and image paths.

Project manifest:
/opt/neandertimeline_project_manifest/neandertimeline_project_manifest.json

Files that may need patching:
/opt/neandertimeline_modular
/opt/neandertimeline_modular/neandertimeline_app.py
/opt/neandertimeline_modular/neandertimeline_modules/
/opt/neandertimeline_modular/config.json
/home/we6jbo/.local/bin/neandertimeline

The patch must make sure these paths are owned by:
we6jbo:we6jbo

Prefer a terminal-paste patch script.

If using a download file, include:

mkdir -p /tmp/patch_file
mv /home/we6jbo/Downloads/{{Name of patch file}} /tmp/patch_file/
cd /tmp/patch_file
chmod +x {{Name of patch file}}
./{{Name of patch file}}
"""

