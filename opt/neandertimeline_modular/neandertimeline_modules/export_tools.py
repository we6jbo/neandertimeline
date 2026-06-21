import shutil, subprocess, os
from pathlib import Path
from PIL import Image, ImageDraw
from .paths import STATE_FILE, CLICK_JSON, GENEALOGY_JSON, IMAGE_DIR
class ExportToolsModule:
    module_name='export_tools'
    def portable_export(self,target_dir,source_root):
        target=Path(target_dir); app=target/'neandertimeline_portable'
        if app.exists(): shutil.rmtree(app)
        app.mkdir(parents=True)
        shutil.copytree(Path(source_root)/'neandertimeline_modules', app/'neandertimeline_modules')
        shutil.copy2(Path(source_root)/'neandertimeline_app.py', app/'neandertimeline_app.py')
        data=app/'data'; data.mkdir()
        for p in [STATE_FILE,CLICK_JSON,GENEALOGY_JSON]:
            if Path(p).exists(): shutil.copy2(p,data/Path(p).name)
        if IMAGE_DIR.exists(): shutil.copytree(IMAGE_DIR, app/'sample')
        (app/'RUN_WINDOWS.bat').write_text('@echo off\npython neandertimeline_app.py\npause\n',encoding='utf-8')
        return str(app)
    def make_mp4_to_usb(self,target_dir,state):
        out=Path(target_dir)/'neandertimeline_mp4_export'; frames=out/'frames'
        if out.exists(): shutil.rmtree(out)
        frames.mkdir(parents=True)
        for i,sc in enumerate(state.get('scenes',[])):
            img=Image.new('RGB',(1280,720),(245,241,233)); d=ImageDraw.Draw(img); d.text((50,40),sc.get('title',''),fill=(0,0,0)); d.text((50,80),sc.get('year',''),fill=(0,0,0)); y=130
            for line in (sc.get('text',[])+sc.get('people_lines',[]))[:10]: d.text((50,y),str(line)[:130],fill=(0,0,0)); y+=35
            img.save(frames/f'frame_{i:04d}.png')
        mp4=out/'neandertimeline.mp4'
        if shutil.which('ffmpeg'):
            subprocess.check_call(['ffmpeg','-y','-framerate','1','-i',str(frames/'frame_%04d.png'),'-c:v','libx264','-pix_fmt','yuv420p',str(mp4)])
            return str(mp4)
        return 'ffmpeg not installed. Install with: sudo apt install ffmpeg'

