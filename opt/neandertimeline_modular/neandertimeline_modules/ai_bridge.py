import os
import shutil
from datetime import datetime
from pathlib import Path
from .paths import (
    AI_REQUEST_FILE,
    AI_PATCH_FILE,
    STATE_FILE,
    OPT_CONFIG,
    OPT_DIR,
    PROJECT_MANIFEST_JSON,
    GOOGLE_AI_PROMPT_FILE,
)
from .storage import write_json, read_json, load_config, save_config, patch_request_text

class AIBridgeModule:
    module_name = "ai_bridge"

    def __init__(self):
        self.config = load_config()

    def key_status(self):
        keys = [self.config.get("google_ai_key_env", "GOOGLE_API_KEY")]
        keys += self.config.get("fallback_ai_key_envs", [])
        return {
            "enabled": bool(self.config.get("free_online_ai_ok")) or os.environ.get("FREE_ONLINE_AI_OK") == "1",
            "key_envs_found": [k for k in keys if os.environ.get(k)],
        }

    def set_online_ai_enabled(self, enabled):
        self.config["free_online_ai_ok"] = bool(enabled)
        save_config(self.config)

    def safe_module_export(self, name, module, state):
        try:
            if name == "magnet":
                return module.export_for_ai(state.get("scenes", []))
            return module.export_for_ai()
        except TypeError:
            try:
                return module.export_for_ai(state.get("scenes", []))
            except Exception as e:
                return {"module": name, "export_error": str(e)}
        except Exception as e:
            return {"module": name, "export_error": str(e)}

    def validate_ai_patch(self, patch):
        if not isinstance(patch, dict):
            return False, "Patch must be a JSON object."

        forbidden_keys = [
            "replace_app",
            "overwrite_app",
            "shell_script",
            "bash",
            "cat_to_neandertimeline_app",
            "delete_files",
        ]
        for key in forbidden_keys:
            if key in patch:
                return False, f"Rejected destructive patch key: {key}"

        scenes = patch.get("scenes")
        if scenes is None:
            return False, "Patch rejected. It must include a scenes list. I will not overwrite the timeline with non-scene data."

        if not isinstance(scenes, list) or len(scenes) < 5:
            return False, "Patch rejected. scenes must be a list with at least 5 scenes."

        for idx, scene in enumerate(scenes):
            if not isinstance(scene, dict):
                return False, f"Patch rejected. Scene {idx} is not an object."
            if "title" not in scene or "map" not in scene or "image" not in scene:
                return False, f"Patch rejected. Scene {idx} must include title, map, and image."
            if not str(scene.get("map", "")).startswith("/home/we6jbo/"):
                return False, f"Patch rejected. Scene {idx} map must be a /home/we6jbo path."
            if not str(scene.get("image", "")).startswith("/home/we6jbo/"):
                return False, f"Patch rejected. Scene {idx} image must be a /home/we6jbo path."

        return True, "Patch validated."

    def build_google_ai_prompt_text(self, state, modules):
        status = self.key_status()
        return f"""
Return your entire response as a single paste-ready bash script block wrapped inside:

cat > /tmp/neandertimeline_patch.sh <<'NEANDER_PATCH_SCRIPT'
#!/usr/bin/env bash
set -euo pipefail
...
NEANDER_PATCH_SCRIPT
chmod +x /tmp/neandertimeline_patch.sh
/tmp/neandertimeline_patch.sh

Strict Constraints:
Do not include any explanations, markdown comments outside the script, conversational filler, or multiple code blocks.
Remove any numbered section headers or numbered comments from the code comments.
Right before generating the AI patch data payloads, add this command-line check to execute the restore-point creation command if it exists:

if command -v createneanderthalrestorepoint &> /dev/null; then createneanderthalrestorepoint; fi

The response must be only the paste-ready bash script.

GOOGLE AI TASK FOR NEANDERTIMELINE

I have a copy of the code for this project available at https://github.com/we6jbo/neandertimeline


You are helping improve Jeremiah O'Neal's existing NeanderTimeline Python/Tk program.


TERMINAL PATCH OUTPUT REQUIREMENT:

You must give Jeremiah exactly one complete terminal-paste bash script wrapped with the NEANDER_PATCH_SCRIPT heredoc.

Do not explain what we could do.
Do not give separate code blocks.
Do not give Python snippets by themselves.
Do not give a plan.
Do not say "here is what we could do."
Do not include explanation before or after the script. Do not use markdown outside the script.

Your entire answer must be one terminal-paste script.

The script must start with this exact pattern, but use a safe unique heredoc marker:

cat > /tmp/neandertimeline_patch.sh <<'NEANDER_PATCH_SCRIPT'
#!/usr/bin/env bash
set -euo pipefail

The script must end with this exact pattern:

NEANDER_PATCH_SCRIPT
chmod +x /tmp/neandertimeline_patch.sh
/tmp/neandertimeline_patch.sh

Before changing anything, the script must create backups in:
~/.neanderthal_23andme_2026/living_timeline/backups

The patch script must not delete images.
The patch script must not delete map click JSON.
The patch script must not delete genealogy TG JSON.
The patch script must not replace the full Tk map/timeline GUI with a small button-only GUI.
The patch script must not remove the map canvas.
The patch script must not remove Back, Play, Next, AI Improve, Write Google AI Prompt, Apply AI Patch, Export, or Make MP4.
The patch script must not overwrite living_timeline_state.json with non-scene data.

If the patch changes Python code, it must run:

python3 -m py_compile /opt/neandertimeline_modular/neandertimeline_app.py
python3 -m py_compile /opt/neandertimeline_modular/neandertimeline_modules/*.py

The script must end by running:

sudo chown -R we6jbo:we6jbo /opt/neandertimeline_modular /opt/neandertimeline_project_manifest
sudo chmod -R u+rwX,go+rX /opt/neandertimeline_modular /opt/neandertimeline_project_manifest

The script must print:

Patch complete.
Run: neandertimeline

CRITICAL SAFETY RULES:
1. Do NOT overwrite /opt/neandertimeline_modular/neandertimeline_app.py.
2. Do NOT replace the app with a small button-only GUI.
3. Do NOT remove the map canvas.
4. Do NOT remove the timeline playback.
5. Do NOT remove Back, Play, Next, AI Improve, Apply AI Patch, Export, or Make MP4.
6. Do NOT overwrite config.json with a tiny config that deletes existing keys.
7. Do NOT overwrite the project manifest with a tiny manifest.
8. Do NOT overwrite living_timeline_state.json with non-scene data.
9. You may write only ai_patch.json unless Jeremiah explicitly asks for a code patch.
10. ai_patch.json must include a valid scenes list. Each scene must have title, map, image, text, people_lines, point_labels, route_labels, and tags where possible.

Your safe output should normally be:
~/.neanderthal_23andme_2026/living_timeline/ai_patch.json

Project manifest:
{PROJECT_MANIFEST_JSON}

Installed app:
{OPT_DIR}

Config:
{OPT_CONFIG}

Living state:
{STATE_FILE}

AI request package:
{AI_REQUEST_FILE}

AI patch file:
{AI_PATCH_FILE}

Google AI prompt file:
{GOOGLE_AI_PROMPT_FILE}

Module imports:
from neandertimeline_modules.map_timeline import MapTimelineModule
from neandertimeline_modules.graphics_timeline import GraphicsTimelineModule
from neandertimeline_modules.people_tg import PeopleTGModule
from neandertimeline_modules.magnet import MagnetEngine
from neandertimeline_modules.ai_bridge import AIBridgeModule
from neandertimeline_modules.export_tools import ExportToolsModule

Module use:
m = MapTimelineModule()
click_points = m.click_points

g = GraphicsTimelineModule()
assets = g.asset_status()

p = PeopleTGModule()
people = p.get_reference_marks()

mag = MagnetEngine()
links = mag.links_for_scene(current_scene)

Current AI status:
{status}


GitHub project copy:
https://github.com/we6jbo/neandertimeline

When suggesting patches, assume Jeremiah may compare the local files against this GitHub copy.
Do not tell Jeremiah to overwrite the local project from GitHub unless explicitly asked.
Prefer safe, surgical terminal-paste patches.

Recommended version storage:
~/.neanderthal_23andme_2026/living_timeline/versions

Required patch behavior:
Before applying changes, create a backup of living_timeline_state.json.
Never delete user images.
Never delete click-coordinate JSON.
Never delete genealogy TG JSON.
Never delete the map timeline.
Never delete the Tk map canvas.

If you provide a terminal patch, it must be surgical and must be one complete paste-ready bash script.
It must patch only the needed function or file.
It must not use `cat > /opt/neandertimeline_modular/neandertimeline_app.py` unless the full original map/timeline app is preserved.
It must not wipe out features.

The correct goal:
Make the Google AI button eventually communicate directly with Google AI, improve the living timeline, create safe versions, and allow downgrade.
"""

    def build_ai_request_package(self, state, modules):
        module_exports = {
            name: self.safe_module_export(name, module, state)
            for name, module in modules.items()
            if hasattr(module, "export_for_ai")
        }
        prompt = self.build_google_ai_prompt_text(state, modules)
        GOOGLE_AI_PROMPT_FILE.parent.mkdir(parents=True, exist_ok=True)
        GOOGLE_AI_PROMPT_FILE.write_text(prompt, encoding="utf-8")

        package = {
            "created": datetime.now().isoformat(timespec="seconds"),
            "goal": "Safely improve NeanderTimeline without wiping features.",
            "safeguards": [
                "Do not overwrite main app.",
                "Do not remove map canvas.",
                "Do not remove timeline controls.",
                "Only write ai_patch.json unless code patch is explicitly requested.",
                "ai_patch.json must include valid scenes with map and image paths."
            ],
            "google_ai_prompt_file": str(GOOGLE_AI_PROMPT_FILE),
            "project_manifest": str(PROJECT_MANIFEST_JSON),
            "state_file": str(STATE_FILE),
            "opt_config": str(OPT_CONFIG),
            "ai_patch_file_to_write": str(AI_PATCH_FILE),
            "current_state": state,
            "module_exports": module_exports,
            "google_ai_status": self.key_status(),
            "prompt_text": prompt,
        }
        write_json(AI_REQUEST_FILE, package)
        return package

    def write_google_ai_prompt(self, state, modules):
        package = self.build_ai_request_package(state, modules)
        return package["google_ai_prompt_file"]

    def apply_patch_file_if_present(self, state):
        patch = read_json(AI_PATCH_FILE, None)
        if not patch:
            return state, "No ai_patch.json found."

        ok, msg = self.validate_ai_patch(patch)
        if not ok:
            reject_file = AI_PATCH_FILE.with_name("ai_patch.rejected.json")
            write_json(reject_file, patch)
            return state, msg + f" Rejected patch saved to {reject_file}"

        versions = STATE_FILE.parent / "versions"
        versions.mkdir(parents=True, exist_ok=True)
        if STATE_FILE.exists():
            backup = versions / f"living_timeline_state.before_ai_patch_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            shutil.copy2(STATE_FILE, backup)

        state["scenes"] = patch["scenes"]
        if "notes" in patch:
            state["notes"] = patch["notes"]

        state.setdefault("ai_revision_history", []).append(
            {
                "applied": datetime.now().isoformat(timespec="seconds"),
                "source": str(AI_PATCH_FILE),
                "summary": patch.get("summary", "Applied safe AI patch."),
            }
        )

        return state, "Applied safe ai_patch.json."

    def paste_to_chatgpt_solution(self, error_text=""):
        return patch_request_text(error_text)

