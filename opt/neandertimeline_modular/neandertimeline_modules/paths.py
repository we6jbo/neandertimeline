from pathlib import Path

APP_NAME = "neandertimeline_modular"

OPT_DIR = Path("/opt/neandertimeline_modular")
OPT_CONFIG = OPT_DIR / "config.json"

PROJECT_MANIFEST_DIR = Path("/opt/neandertimeline_project_manifest")
PROJECT_MANIFEST_JSON = PROJECT_MANIFEST_DIR / "neandertimeline_project_manifest.json"

DATA_DIR = Path("~/.neanderthal_23andme_2026")
STATE_DIR = DATA_DIR / "living_timeline"
STATE_FILE = STATE_DIR / "living_timeline_state.json"
AI_REQUEST_FILE = STATE_DIR / "ai_request_package.json"
AI_PATCH_FILE = STATE_DIR / "ai_patch.json"
GOOGLE_AI_PROMPT_FILE = STATE_DIR / "google_ai_prompt.txt"
DEBUG_LOG = STATE_DIR / "neandertimeline_modular_debug.log"

IMAGE_DIR = Path("./sample_assets")
CLICK_JSON = DATA_DIR / "neanderthal_click_capture.json"
GENEALOGY_JSON = DATA_DIR / "genealogy_tg_associations.json"

MAP_MIGRATION = IMAGE_DIR / "Map-base-europe-middle-east-centrial-asia-map.png"
MAP_REGIONAL = IMAGE_DIR / "map-base-africa-europe-asia-migration-map.png"

IMG_23ANDME = IMAGE_DIR / "23andme-neanderthal-result.png"
IMG_HELIX = IMAGE_DIR / "DNA-Genetics-DNA-Helix-Image.png"
IMG_ICE_AGE = IMAGE_DIR / "Culture-Survival-Ice-Age-Landscape.png"
IMG_TOOLS = IMAGE_DIR / "Culture-tools-mousterian-stone-tools.png"
IMG_DENISOVA = IMAGE_DIR / "Fossil-Archaeological-site-image-denisova-cave-altai.png"
IMG_FELDHOFER = IMAGE_DIR / "Fossil-archaeological-site-image-neander-valley-feldhofer-cave.png"
IMG_VINDIJA = IMAGE_DIR / "Fossil-Archaological-site-image-vindija-cave-croatia.png"

ALL_ASSETS = {
    "map_migration": MAP_MIGRATION,
    "map_regional": MAP_REGIONAL,
    "23andme": IMG_23ANDME,
    "helix": IMG_HELIX,
    "ice_age": IMG_ICE_AGE,
    "tools": IMG_TOOLS,
    "denisova": IMG_DENISOVA,
    "feldhofer": IMG_FELDHOFER,
    "vindija": IMG_VINDIJA,
}

