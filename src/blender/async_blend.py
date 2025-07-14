import os
import asyncio

# --- Config ---
WATCHED_IMAGE = os.path.join(os.path.dirname(__file__), '../../assets/images/label.png')
BLEND_FILE = os.path.join(os.path.dirname(__file__), '../../assets/blend_files/golf_scene.blend')
GEN_SCRIPT = os.path.join(os.path.dirname(__file__), 'generate_label_glb.py')
GLB_OUTPUT = os.path.join(os.path.dirname(__file__), '../../assets/models/output.glb')
BLENDER_DIR = r"C:\Program Files\Blender Foundation\Blender 4.4"
BLENDER_EXE = os.path.join(BLENDER_DIR, "blender.exe")

last_mtime = None

async def watch_file():
    global last_mtime
    while True:
        try:
            current_mtime = os.path.getmtime(WATCHED_IMAGE)
            if last_mtime is None:
                last_mtime = current_mtime
            elif current_mtime != last_mtime:
                print("[INFO] Detected change in image. Rebuilding GLB...")
                last_mtime = current_mtime
                await run_blender_export()
        except FileNotFoundError:
            print("[WARN] Watched file not found.")
        await asyncio.sleep(2)

async def run_blender_export():
    command = [
        BLENDER_EXE, BLEND_FILE,
        "--background",
        "--python", GEN_SCRIPT,
        "--", WATCHED_IMAGE, GLB_OUTPUT
    ]
    process = await asyncio.create_subprocess_exec(*command, cwd=BLENDER_DIR)
    await process.communicate()
    print("[INFO] Blender export complete.")

if __name__ == "__main__":
    print(f"[INFO] Watching {WATCHED_IMAGE} for changes...")
    asyncio.run(watch_file())
