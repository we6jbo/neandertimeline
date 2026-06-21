from datetime import datetime
from .paths import (
    MAP_MIGRATION,
    MAP_REGIONAL,
    IMG_23ANDME,
    IMG_HELIX,
    IMG_ICE_AGE,
    IMG_TOOLS,
    IMG_DENISOVA,
    IMG_FELDHOFER,
    IMG_VINDIJA,
)
from .people_tg import PeopleTGModule

def S(path_obj):
    """Return a JSON-safe string path."""
    return str(path_obj)

def build_default_scenes():
    people_module = PeopleTGModule()

    def person_lines(region):
        return people_module.text_lines_for_region(region, 12)

    scenes = [
        {
            "id": "scene_1978_birth",
            "year": "03/24/1978",
            "title": "Jeremiah Burke O'Neal is born",
            "map": S(MAP_MIGRATION),
            "image": S(IMG_23ANDME),
            "point_labels": [],
            "route_labels": [],
            "text": [
                "This timeline starts with Jeremiah's birth date and then walks backward through family tree regions and older context."
            ],
            "people_lines": [],
            "tags": ["start", "jeremiah", "modern"],
        },
        {
            "id": "scene_2026_23andme",
            "year": "2026",
            "title": "23andMe Neanderthal result",
            "map": S(MAP_MIGRATION),
            "image": S(IMG_23ANDME),
            "point_labels": [],
            "route_labels": [],
            "text": [
                "Jeremiah's 2026 23andMe result is the modern DNA starting point for this timeline.",
                "Project wording: top 89 percent / 89th percentile among 23andMe customers for Neanderthal variants.",
            ],
            "people_lines": [],
            "tags": ["dna", "23andme", "modern"],
        },
        {
            "id": "scene_british_isles",
            "year": "1700s-1900s",
            "title": "British Isles family lines",
            "map": S(MAP_REGIONAL),
            "image": S(IMG_FELDHOFER),
            "point_labels": ["British Isles family-history overlay"],
            "route_labels": ["British Isles family-history overlay"],
            "text": [
                "Family lines in the notes include Scotland, England, Ireland, County Down, Newry, Cumberland, and Cockermouth."
            ],
            "people_lines": person_lines("British Isles"),
            "tags": ["family", "old_world", "british_isles"],
        },
        {
            "id": "scene_german_central",
            "year": "1700s-1900s",
            "title": "German-speaking Central Europe lines",
            "map": S(MAP_REGIONAL),
            "image": S(IMG_HELIX),
            "point_labels": ["German-speaking family-history overlay"],
            "route_labels": ["German-speaking family-history overlay"],
            "text": [
                "Family lines in the notes include Baden-Württemberg, Württemberg, Waldshut, Stuttgart, and related German-speaking areas."
            ],
            "people_lines": person_lines("German-speaking Central Europe"),
            "tags": ["family", "old_world", "germany"],
        },
        {
            "id": "scene_prussia_pomerania",
            "year": "1700s-1900s",
            "title": "Prussia, Pomerania, and Schleswig-Holstein lines",
            "map": S(MAP_REGIONAL),
            "image": S(IMG_VINDIJA),
            "point_labels": ["West Prussia / Pomerania overlay"],
            "route_labels": ["West Prussia / Pomerania overlay"],
            "text": [
                "Family lines in the notes include West Prussia, Pomerania, Schleswig-Holstein, Tondern, Danzig, Berent, and Paleschken."
            ],
            "people_lines": person_lines("Prussia / Pomerania / Schleswig-Holstein"),
            "tags": ["family", "old_world", "prussia", "pomerania"],
        },
        {
            "id": "scene_black_sea_odessa",
            "year": "1700s-1900s",
            "title": "Black Sea / Odessa / Kherson lines",
            "map": S(MAP_MIGRATION),
            "image": S(IMG_DENISOVA),
            "point_labels": ["Black Sea German / Odessa overlay"],
            "route_labels": ["Black Sea German / Odessa overlay"],
            "text": [
                "Family lines in the notes include Odessa, Kherson, Cherson, Neuberg, Lustdorf, Alexanderhilf, Grossliebental, and related Black Sea German colony regions."
            ],
            "people_lines": person_lines("Black Sea / Odessa / Kherson region"),
            "tags": ["family", "old_world", "odessa", "kherson", "russia"],
        },
        {
            "id": "scene_africa_to_levant",
            "year": "about 70,000-50,000 years ago",
            "title": "Older route context: Africa toward Eurasia",
            "map": S(MAP_MIGRATION),
            "image": S(IMG_ICE_AGE),
            "point_labels": [
                "East Africa origin context",
                "Northeast Africa corridor",
                "Sinai / Levant crossing",
            ],
            "route_labels": [
                "East Africa origin context",
                "Northeast Africa corridor",
                "Sinai / Levant crossing",
            ],
            "text": [
                "The timeline moves from named family-tree regions into older human-history context using the clicked map points."
            ],
            "people_lines": [],
            "tags": ["ancient", "route", "africa", "levant"],
        },
        {
            "id": "scene_levant_europe",
            "year": "roughly 50,000-40,000 years ago",
            "title": "Levant and Europe entry context",
            "map": S(MAP_MIGRATION),
            "image": S(IMG_TOOLS),
            "point_labels": [
                "Levant admixture zone",
                "Anatolia bridge",
                "Balkan Europe entry",
                "Central Europe Neanderthal context",
                "Western Europe branch",
            ],
            "route_labels": [
                "Sinai / Levant crossing",
                "Levant admixture zone",
                "Anatolia bridge",
                "Balkan Europe entry",
                "Central Europe Neanderthal context",
                "Western Europe branch",
            ],
            "text": [
                "This uses the plotted Levant, Anatolia, Balkan, Central Europe, and Western Europe points."
            ],
            "people_lines": [],
            "tags": ["ancient", "route", "neanderthal", "europe"],
        },
        {
            "id": "scene_sites",
            "year": "Neanderthal site context",
            "title": "Neander Valley and Vindija Cave",
            "map": S(MAP_REGIONAL),
            "image": S(IMG_FELDHOFER),
            "point_labels": [
                "Neander Valley / Feldhofer context",
                "Vindija Cave context",
            ],
            "route_labels": [
                "Neander Valley / Feldhofer context",
                "Vindija Cave context",
            ],
            "text": [
                "This scene shows the archaeological context points that were plotted."
            ],
            "people_lines": [],
            "tags": ["ancient", "sites", "neanderthal"],
        },
        {
            "id": "scene_altai",
            "year": "Deep archaic-human context",
            "title": "Denisova / Altai direction",
            "map": S(MAP_REGIONAL),
            "image": S(IMG_DENISOVA),
            "point_labels": ["Central Asia / Denisova direction"],
            "route_labels": ["Central Asia / Denisova direction"],
            "text": [
                "This scene uses the Central Asia / Denisova direction point as broader archaic-human context."
            ],
            "people_lines": [],
            "tags": ["ancient", "altai", "denisova"],
        },
    ]
    return scenes

def default_state():
    return {
        "state_version": 1,
        "created": datetime.now().isoformat(timespec="seconds"),
        "updated": datetime.now().isoformat(timespec="seconds"),
        "scene_index": 0,
        "scenes": build_default_scenes(),
        "ai_revision_history": [],
        "module_magnet_links": [],
        "notes": "Living timeline state. Edits are persisted here and reloaded without asking AI again."
    }

