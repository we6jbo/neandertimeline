class MagnetEngine:
    module_name = "magnet"

    def __init__(self):
        self.rules = [
            {
                "when_tag": "old_world",
                "attract": ["map_timeline", "people_tg", "graphics_timeline"],
                "reason": "old-world family lines need map location, names/TGs, and image context",
            },
            {
                "when_tag": "ancient",
                "attract": ["map_timeline", "graphics_timeline"],
                "reason": "ancient context needs map route and supporting graphics",
            },
            {
                "when_tag": "dna",
                "attract": ["graphics_timeline", "people_tg", "ai_bridge"],
                "reason": "DNA scene connects image, family references, and AI revision",
            },
            {
                "when_tag": "route",
                "attract": ["map_timeline", "ai_bridge"],
                "reason": "route scenes can be improved by checking coordinates and narrative order",
            },
        ]

    def links_for_scene(self, scene):
        tags = set(scene.get("tags", []))
        links = []
        for rule in self.rules:
            if rule["when_tag"] in tags:
                links.append(
                    {
                        "scene_id": scene.get("id"),
                        "attract": rule["attract"],
                        "reason": rule["reason"],
                    }
                )
        return links

    def export_for_ai(self, scenes=None):
        if scenes is None:
            scenes = []
        magnet_links = []
        for scene in scenes:
            magnet_links.extend(self.links_for_scene(scene))
        return {
            "module": self.module_name,
            "rules": self.rules,
            "magnet_links": magnet_links,
        }

