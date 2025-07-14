import bpy
import sys
import os

# --- CONFIG ---
NEW_IMAGE_PATH = "C:/Users/Shriansh/Desktop/SPT/Golf Image/3D/image.png"  # Change this
OUTPUT_GLB_PATH = "C:/Users/Shriansh/Desktop/SPT/Golf Image/3D/exported_label.glb" # Change this
TARGET_MATERIAL_NAME = "Material.002"  # Change if your material name is different
TARGET_OBJECT_NAME = "Cylinder"        # The name of the label object

# --- LOAD IMAGE ---
def update_material_image():
    mat = bpy.data.materials.get(TARGET_MATERIAL_NAME)
    if not mat:
        raise ValueError(f"Material '{TARGET_MATERIAL_NAME}' not found.")

    # Go into node tree
    nodes = mat.node_tree.nodes
    for node in nodes:
        if node.type == 'TEX_IMAGE':
            # Load or reuse the image
            if node.image:
                bpy.data.images.remove(node.image)
            img = bpy.data.images.load(NEW_IMAGE_PATH)
            node.image = img
            print(f"[INFO] Updated image texture to: {NEW_IMAGE_PATH}")
            return
    raise RuntimeError("No image texture node found in material.")

# --- EXPORT TO GLB ---
def export_glb():
    bpy.ops.export_scene.gltf(filepath=OUTPUT_GLB_PATH, export_format='GLB')
    print(f"[INFO] Exported .glb to {OUTPUT_GLB_PATH}")

# --- MAIN ---
if __name__ == "__main__":
    update_material_image()
    export_glb()
