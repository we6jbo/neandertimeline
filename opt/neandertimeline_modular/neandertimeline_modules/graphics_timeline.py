from .paths import ALL_ASSETS
class GraphicsTimelineModule:
    module_name='graphics_timeline'
    def __init__(self): self.assets=ALL_ASSETS
    def asset_status(self): return {k:{'path':str(v),'exists':v.exists()} for k,v in self.assets.items()}
    def export_for_ai(self): return {'module':self.module_name,'assets':self.asset_status()}

