from .paths import CLICK_JSON, MAP_REGIONAL, MAP_MIGRATION
from .storage import read_json
def load_click_points(data=None):
    if data is None: data=read_json(CLICK_JSON,{})
    captures=data.get('click_captures',[]) if isinstance(data,dict) else []
    pts={}
    for cap in captures:
        guide=cap.get('guide_item',{})
        label=guide.get('label') or cap.get('label')
        if not label: continue
        try: x=int(cap.get('click_original_image_x')); y=int(cap.get('click_original_image_y'))
        except Exception: continue
        pts[label]={'label':label,'x':x,'y':y,'map_name':cap.get('map_name',''),'area':guide.get('country_or_area','')}
    return pts
class MapTimelineModule:
    module_name='map_timeline'
    def __init__(self): self.click_points=load_click_points()
    def get_points_for_labels(self,labels): return [self.click_points[l] for l in labels if l in self.click_points]
    def get_route_for_scene(self,scene): return self.get_points_for_labels(scene.get('route_labels',[]))
    def export_for_ai(self): return {'module':self.module_name,'click_points':self.click_points,'maps':{'migration':str(MAP_MIGRATION),'regional':str(MAP_REGIONAL)}}

