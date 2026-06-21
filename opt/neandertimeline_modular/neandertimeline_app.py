#!/usr/bin/env python3
import sys
import traceback
import subprocess
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk, ImageDraw

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from neandertimeline_modules.paths import STATE_FILE, AI_REQUEST_FILE, AI_PATCH_FILE, GOOGLE_AI_PROMPT_FILE, PROJECT_MANIFEST_JSON
from neandertimeline_modules.storage import load_state, save_state, patch_request_text
from neandertimeline_modules.scenes import default_state
from neandertimeline_modules.map_timeline import MapTimelineModule
from neandertimeline_modules.graphics_timeline import GraphicsTimelineModule
from neandertimeline_modules.people_tg import PeopleTGModule
from neandertimeline_modules.magnet import MagnetEngine
from neandertimeline_modules.ai_bridge import AIBridgeModule
from neandertimeline_modules.export_tools import ExportToolsModule

def show_copyable_error(root, error_text):
    full_text = patch_request_text(error_text)
    win = tk.Toplevel(root)
    win.title("NeanderTimeline Error")
    win.geometry("1000x700")
    win.configure(bg="#202020")

    header = tk.Label(
        win,
        text="Google AI, the following error occurred. Copy this and ask for a terminal patch script.",
        bg="#202020",
        fg="white",
        font=("Arial", 14, "bold"),
        wraplength=960,
        justify="left",
        anchor="w",
    )
    header.pack(fill=tk.X, padx=12, pady=(12, 6))

    box = scrolledtext.ScrolledText(win, wrap=tk.WORD, bg="#111111", fg="#eeeeee", insertbackground="white", font=("Courier", 10))
    box.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)
    box.insert(tk.END, full_text)

    def copy_all():
        win.clipboard_clear()
        win.clipboard_append(full_text)
        win.update()
        copy_btn.config(text="Copied to clipboard")

    btns = tk.Frame(win, bg="#202020")
    btns.pack(fill=tk.X, padx=12, pady=(0, 12))
    copy_btn = tk.Button(btns, text="Copy to Clipboard", command=copy_all, width=22)
    copy_btn.pack(side=tk.LEFT)
    tk.Button(btns, text="Close", command=win.destroy, width=12).pack(side=tk.LEFT, padx=8)

def install_tk_exception_handler(root):
    def report_callback_exception(exc, val, tb):
        error_text = "".join(traceback.format_exception(exc, val, tb))
        show_copyable_error(root, error_text)
    root.report_callback_exception = report_callback_exception

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Jeremiah’s Neanderthal and Family Timeline Viewer")
        self.root.geometry("1450x880")
        self.root.configure(bg="#202020")

        self.state = load_state(default_state())
        self.idx = int(self.state.get("scene_index", 0))
        self.playing = False
        self.after_id = None

        self.modules = {
            "map_timeline": MapTimelineModule(),
            "graphics_timeline": GraphicsTimelineModule(),
            "people_tg": PeopleTGModule(),
            "magnet": MagnetEngine(),
            "ai_bridge": AIBridgeModule(),
            "export_tools": ExportToolsModule(),
        }

        self.current_map_tk = None
        self.current_side_tk = None
        self.map_draw_info = None

        self.build_ui()
        self.render()

    def build_ui(self):
        main = tk.Frame(self.root, bg="#202020")
        main.pack(fill=tk.BOTH, expand=True)

        left = tk.Frame(main, bg="#111111")
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        right = tk.Frame(main, bg="#2b2b2b", width=470)
        right.pack(side=tk.RIGHT, fill=tk.Y)
        right.pack_propagate(False)

        self.canvas = tk.Canvas(left, bg="#111111", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.title_lbl = tk.Label(right, text="", bg="#2b2b2b", fg="white", font=("Arial", 16, "bold"), wraplength=440, justify="left", anchor="w")
        self.title_lbl.pack(fill=tk.X, padx=12, pady=(12, 4))

        self.year_lbl = tk.Label(right, text="", bg="#2b2b2b", fg="#66ccff", font=("Arial", 13, "bold"), wraplength=440, justify="left", anchor="w")
        self.year_lbl.pack(fill=tk.X, padx=12, pady=(0, 8))

        self.side_img_lbl = tk.Label(right, bg="#2b2b2b")
        self.side_img_lbl.pack(fill=tk.X, padx=12, pady=6)

        self.text_box = tk.Text(right, bg="#1f1f1f", fg="#eeeeee", font=("Arial", 11), wrap=tk.WORD, height=10, relief=tk.FLAT, padx=8, pady=8)
        self.text_box.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)

        self.people_box = tk.Text(right, bg="#111111", fg="#b8ffb8", font=("Courier", 9), wrap=tk.WORD, height=10, relief=tk.FLAT, padx=8, pady=8)
        self.people_box.pack(fill=tk.X, padx=12, pady=(0, 8))

        controls = tk.Frame(right, bg="#2b2b2b")
        controls.pack(fill=tk.X, padx=12, pady=4)

        tk.Button(controls, text="◀ Back", command=self.prev_scene, width=9).pack(side=tk.LEFT)
        self.play_btn = tk.Button(controls, text="Play", command=self.toggle_play, width=9)
        self.play_btn.pack(side=tk.LEFT, padx=5)
        tk.Button(controls, text="Next ▶", command=self.next_scene, width=9).pack(side=tk.LEFT)

        controls2 = tk.Frame(right, bg="#2b2b2b")
        controls2.pack(fill=tk.X, padx=12, pady=4)

        tk.Button(controls2, text="AI Improve", command=self.ai_improve, width=11).pack(side=tk.LEFT)
        tk.Button(controls2, text="Write Google AI Prompt", command=self.write_google_ai_prompt, width=20).pack(side=tk.LEFT, padx=5)

        controls3 = tk.Frame(right, bg="#2b2b2b")
        controls3.pack(fill=tk.X, padx=12, pady=4)

        tk.Button(controls3, text="Apply AI Patch", command=self.apply_ai_patch, width=13).pack(side=tk.LEFT)
        tk.Button(controls3, text="Export", command=self.export_portable, width=9).pack(side=tk.LEFT, padx=5)
        tk.Button(controls3, text="Make MP4", command=self.make_mp4, width=10).pack(side=tk.LEFT)

        controls4 = tk.Frame(right, bg="#2b2b2b")
        controls4.pack(fill=tk.X, padx=12, pady=4)

        tk.Button(controls4, text="Patch Help Text", command=self.patch_help_text, width=18).pack(side=tk.LEFT)
        tk.Button(controls4, text="Restore Point GUI", command=self.open_restore_gui, width=18).pack(side=tk.LEFT, padx=5)

        self.counter_lbl = tk.Label(right, text="", bg="#2b2b2b", fg="#cccccc", font=("Arial", 10))
        self.counter_lbl.pack(fill=tk.X, padx=12, pady=(4, 2))

        self.status_lbl = tk.Label(right, text="", bg="#2b2b2b", fg="#aaaaaa", font=("Arial", 8), wraplength=440, justify="left", anchor="w")
        self.status_lbl.pack(fill=tk.X, padx=12, pady=(0, 8))

        self.root.bind("<Left>", lambda e: self.prev_scene())
        self.root.bind("<Right>", lambda e: self.next_scene())
        self.root.bind("<space>", lambda e: self.toggle_play())


    def open_restore_gui(self):
        try:
            subprocess.Popen(["/home/we6jbo/.local/bin/neanderthalrestoregui"])
        except Exception as e:
            show_copyable_error(self.root, "Could not open restore GUI:\n" + str(e))

    def save_living_state(self):
        self.state["scene_index"] = self.idx
        save_state(self.state)

    def load_image(self, path, max_size=None):
        p = Path(str(path))
        if not p.exists():
            img = Image.new("RGB", max_size or (900, 600), "#444444")
            d = ImageDraw.Draw(img)
            d.text((20, 20), f"Missing image:\n{p}", fill="white")
            return img
        img = Image.open(p).convert("RGB")
        if max_size:
            img.thumbnail(max_size, Image.LANCZOS)
        return img

    def scale_map(self, img):
        self.canvas.update_idletasks()
        cw = max(700, self.canvas.winfo_width())
        ch = max(500, self.canvas.winfo_height())
        iw, ih = img.size
        scale = min(cw / iw, ch / ih)
        nw, nh = int(iw * scale), int(ih * scale)
        resized = img.resize((nw, nh), Image.LANCZOS)
        info = {"x0": (cw - nw) // 2, "y0": (ch - nh) // 2, "scale": scale}
        return resized, info

    def map_xy(self, x, y):
        info = self.map_draw_info
        return int(info["x0"] + x * info["scale"]), int(info["y0"] + y * info["scale"])

    def draw_marker(self, x, y, label):
        r = 8
        self.canvas.create_oval(x-r, y-r, x+r, y+r, fill="#ffe600", outline="black", width=2)
        self.canvas.create_line(x-14, y, x+14, y, fill="#ff3333", width=3)
        self.canvas.create_line(x, y-14, x, y+14, fill="#ff3333", width=3)
        self.canvas.create_rectangle(x+12, y-14, x+315, y+18, fill="white", outline="black")
        self.canvas.create_text(x+18, y+2, text=str(label)[:35], fill="black", anchor="w", font=("Arial", 9, "bold"))

    def draw_scene_points(self, scene):
        route = self.modules["map_timeline"].get_route_for_scene(scene)
        coords = []
        for p in route:
            coords.append(self.map_xy(p["x"], p["y"]))
        if len(coords) >= 2:
            flat = []
            for x, y in coords:
                flat.extend([x, y])
            self.canvas.create_line(*flat, fill="#ff3333", width=4, smooth=True)

        for p in self.modules["map_timeline"].get_points_for_labels(scene.get("point_labels", [])):
            x, y = self.map_xy(p["x"], p["y"])
            self.draw_marker(x, y, p["label"])

    def render(self):
        scenes = self.state.get("scenes", [])
        if not scenes:
            return

        self.idx = max(0, min(self.idx, len(scenes) - 1))
        scene = scenes[self.idx]

        self.canvas.delete("all")

        map_img = self.load_image(scene.get("map"))
        resized, self.map_draw_info = self.scale_map(map_img)
        self.current_map_tk = ImageTk.PhotoImage(resized)
        self.canvas.create_image(self.map_draw_info["x0"], self.map_draw_info["y0"], anchor="nw", image=self.current_map_tk)
        self.draw_scene_points(scene)

        self.title_lbl.config(text=scene.get("title", ""))
        self.year_lbl.config(text=scene.get("year", ""))

        side = self.load_image(scene.get("image"), (430, 230))
        self.current_side_tk = ImageTk.PhotoImage(side)
        self.side_img_lbl.config(image=self.current_side_tk)

        self.text_box.config(state=tk.NORMAL)
        self.text_box.delete("1.0", tk.END)
        for t in scene.get("text", []):
            self.text_box.insert(tk.END, str(t) + "\n\n")
        self.text_box.config(state=tk.DISABLED)

        self.people_box.config(state=tk.NORMAL)
        self.people_box.delete("1.0", tk.END)
        self.people_box.insert(tk.END, "People / TG reference marks:\n\n")
        lines = scene.get("people_lines", [])
        if lines:
            for line in lines:
                self.people_box.insert(tk.END, str(line) + "\n")
        else:
            self.people_box.insert(tk.END, "No people/TG references for this scene.")
        self.people_box.config(state=tk.DISABLED)

        self.counter_lbl.config(text=f"Scene {self.idx + 1} of {len(scenes)}")
        self.status_lbl.config(
            text=f"Manifest: {PROJECT_MANIFEST_JSON}\nState: {STATE_FILE}\nAI prompt: {GOOGLE_AI_PROMPT_FILE}"
        )
        self.save_living_state()

    def next_scene(self):
        self.idx = (self.idx + 1) % len(self.state.get("scenes", []))
        self.render()

    def prev_scene(self):
        self.idx = (self.idx - 1) % len(self.state.get("scenes", []))
        self.render()

    def toggle_play(self):
        self.playing = not self.playing
        self.play_btn.config(text="Pause" if self.playing else "Play")
        if self.playing:
            self.play_loop()
        elif self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None

    def play_loop(self):
        if not self.playing:
            return
        self.next_scene()
        self.after_id = self.root.after(3500, self.play_loop)

    def ai_improve(self):
        self.modules["ai_bridge"].build_ai_request_package(self.state, self.modules)
        messagebox.showinfo("AI Improve", f"Saved AI request package:\n{AI_REQUEST_FILE}\n\nGoogle AI can write safe scene-only patch:\n{AI_PATCH_FILE}")

    def write_google_ai_prompt(self):
        prompt_path = self.modules["ai_bridge"].write_google_ai_prompt(self.state, self.modules)
        prompt_text = Path(prompt_path).read_text(encoding="utf-8")

        win = tk.Toplevel(self.root)
        win.title("Google AI Prompt")
        win.geometry("1000x700")

        header = tk.Label(win, text=f"Google AI prompt written to:\n{prompt_path}", font=("Arial", 12, "bold"), anchor="w", justify="left")
        header.pack(fill=tk.X, padx=12, pady=8)

        box = scrolledtext.ScrolledText(win, wrap=tk.WORD, font=("Courier", 10))
        box.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)
        box.insert(tk.END, prompt_text)

        def copy_prompt():
            win.clipboard_clear()
            win.clipboard_append(prompt_text)
            win.update()
            copy_btn.config(text="Copied to clipboard")

        copy_btn = tk.Button(win, text="Copy Google AI Prompt", command=copy_prompt, width=24)
        copy_btn.pack(padx=12, pady=(0, 12))

    def apply_ai_patch(self):
        new_state, msg = self.modules["ai_bridge"].apply_patch_file_if_present(self.state)
        self.state = new_state
        save_state(self.state)
        messagebox.showinfo("Apply AI Patch", msg)
        self.render()

    def patch_help_text(self):
        show_copyable_error(self.root, "Manual patch help requested.")

    def export_portable(self):
        target = filedialog.askdirectory(title="Choose USB drive or export folder")
        if not target:
            return
        out = self.modules["export_tools"].portable_export(target, SCRIPT_DIR)
        messagebox.showinfo("Export complete", f"Portable export saved to:\n{out}")

    def make_mp4(self):
        target = filedialog.askdirectory(title="Choose USB drive or export folder for MP4")
        if not target:
            return
        out = self.modules["export_tools"].make_mp4_to_usb(target, self.state)
        messagebox.showinfo("MP4 result", str(out))

def main():
    root = tk.Tk()
    install_tk_exception_handler(root)
    App(root)
    root.mainloop()

if __name__ == "__main__":
    main()

