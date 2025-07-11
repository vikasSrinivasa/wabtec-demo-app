# import trimesh
# import pyrender
# import os
# import numpy as np
# from PIL import Image

# def render_mesh_from_view(mesh, view_matrix, resolution=(512, 512)):
#     scene = pyrender.Scene()
#     renderable = pyrender.Mesh.from_trimesh(mesh, smooth=False)
#     scene.add(renderable)

#     camera = pyrender.PerspectiveCamera(yfov=np.pi / 3.0)
#     scene.add(camera, pose=view_matrix)

#     light = pyrender.DirectionalLight(color=np.ones(3), intensity=2.0)
#     scene.add(light, pose=view_matrix)

#     r = pyrender.OffscreenRenderer(*resolution)
#     color, _ = r.render(scene)
#     r.delete()
#     return color

# def get_camera_poses():
#     front = np.array([
#         [1, 0, 0, 0],
#         [0, 0, -1, 0],
#         [0, 1, 0, 2.5],
#         [0, 0, 0, 1]
#     ])
#     top = np.array([
#         [1, 0, 0, 0],
#         [0, 1, 0, 0],
#         [0, 0, 1, 2.5],
#         [0, 0, 0, 1]
#     ])
#     iso = np.array([
#         [0.707, 0, 0.707, 1.5],
#         [-0.408, 0.816, 0.408, 1.5],
#         [-0.577, -0.577, 0.577, 2.5],
#         [0, 0, 0, 1]
#     ])
#     return {'front': front, 'top': top, 'isometric': iso}

# def render_glb_views(glb_folder, output_folder):
#     os.makedirs(output_folder, exist_ok=True)
#     views = get_camera_poses()

#     for fname in os.listdir(glb_folder):
#         if not fname.endswith(".glb"):
#             continue

#         file_path = os.path.join(glb_folder, fname)
#         try:
#             mesh = trimesh.load(file_path)

#             # Handle scene
#             if isinstance(mesh, trimesh.Scene):
#                 print(f"📦 Dumping and merging scene meshes from {fname}")
#                 dumped = mesh.dump()
#                 if isinstance(dumped, list):
#                     mesh = trimesh.util.concatenate(dumped)
#                 else:
#                     mesh = dumped

#             # Handle list
#             elif isinstance(mesh, list):
#                 print(f"📦 Concatenating mesh list from {fname}")
#                 mesh = trimesh.util.concatenate(mesh)

#             if not isinstance(mesh, trimesh.Trimesh):
#                 raise ValueError("Result is not a Trimesh after conversion")

#             for view_name, cam_pose in views.items():
#                 img = render_mesh_from_view(mesh, cam_pose)
#                 img_pil = Image.fromarray(img)
#                 out_path = os.path.join(output_folder, f"{os.path.splitext(fname)[0]}_{view_name}.png")
#                 img_pil.save(out_path)
#                 print(f"✅ Saved {out_path}")
#         except Exception as e:
#             print(f"❌ Failed to render {fname}: {e}")

# # Run
# render_glb_views("glb_files", "rendered_images")



# import trimesh
# import os
# from pathlib import Path
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D

# # Folder paths
# glb_dir = Path("glb_files")
# out_dir = Path("rendered_images")
# out_dir.mkdir(exist_ok=True)

# # Camera views: (azimuth, elevation)
# views = {
#     "front": (0, 0),
#     "top": (0, 90),
#     "isometric": (45, 35)
# }

# def render_and_save(mesh: trimesh.Trimesh, model_name: str):
#     mesh = mesh.copy()
#     mesh.apply_translation(-mesh.centroid)
#     mesh.apply_scale(1.0 / max(mesh.extents))

#     points = mesh.vertices

#     for view_name, (azim, elev) in views.items():
#         fig = plt.figure(figsize=(6, 6))
#         ax = fig.add_subplot(111, projection='3d')
#         ax.scatter(points[:, 0], points[:, 1], points[:, 2], s=0.3, c='gray', alpha=0.9)
#         ax.view_init(elev=elev, azim=azim)
#         ax.axis('off')

#         out_path = out_dir / f"{model_name}_{view_name}.png"
#         plt.savefig(out_path, dpi=300, bbox_inches='tight', pad_inches=0)
#         plt.close(fig)

#         print(f"✅ Saved: {out_path}")

# def load_mesh(glb_path: Path):
#     mesh = trimesh.load(glb_path)
#     if isinstance(mesh, trimesh.Scene):
#         print(f"📦 Converting scene to mesh for {glb_path.name}")
#         mesh = mesh.dump()
#     if isinstance(mesh, list):
#         print(f"📦 Merging mesh list for {glb_path.name}")
#         mesh = trimesh.util.concatenate(mesh)
#     if not isinstance(mesh, trimesh.Trimesh):
#         raise ValueError("❌ Could not convert to Trimesh.")
#     return mesh

# # Main loop
# for glb_path in glb_dir.glob("*.glb"):
#     model_name = glb_path.stem
#     try:
#         mesh = load_mesh(glb_path)
#         render_and_save(mesh, model_name)
#     except Exception as e:
#         print(f"❌ Failed to render {glb_path.name}: {e}")


import os
import trimesh
import pyrender
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# Ensure output directory exists
output_dir = "rendered_images"
os.makedirs(output_dir, exist_ok=True)

# Camera poses
VIEW_ANGLES = {
    "front": np.array([
        [1, 0, 0, 0],
        [0, 0, -1, 0],
        [0, 1, 0, 2.5],
        [0, 0, 0, 1]
    ]),
    "top": np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 2.5],
        [0, 0, 0, 1]
    ]),
    "isometric": trimesh.transformations.rotation_matrix(
        np.radians(35), [1, 0, 0]
    ) @ trimesh.transformations.rotation_matrix(
        np.radians(45), [0, 1, 0]
    )
}
VIEW_ANGLES["isometric"][2, 3] = 2.5  # Move camera back for iso

# def render_views(mesh_path):
#     try:
#         scene_or_mesh = trimesh.load(mesh_path)

#         # Convert scene to mesh if needed
#         if isinstance(scene_or_mesh, trimesh.Scene):
#             print(f"📦 Converting scene to mesh for {os.path.basename(mesh_path)}")
#             combined = trimesh.util.concatenate(
#                 [geometry for geometry in scene_or_mesh.dump()]
#             )
#         elif isinstance(scene_or_mesh, list):
#             combined = trimesh.util.concatenate(scene_or_mesh)
#         else:
#             combined = scene_or_mesh

#         # Convert to pyrender mesh
#         mesh = pyrender.Mesh.from_trimesh(combined, smooth=False)

#         # Create scene
#         scene = pyrender.Scene()
#         scene.add(mesh)

#         # Add lights
#         light = pyrender.DirectionalLight(color=np.ones(3), intensity=2.0)
#         scene.add(light)

#         # Renderer
#         renderer = pyrender.OffscreenRenderer(viewport_width=768, viewport_height=768)

#         basename = os.path.splitext(os.path.basename(mesh_path))[0]

#         for view_name, pose in VIEW_ANGLES.items():
#             camera = pyrender.PerspectiveCamera(yfov=np.pi / 3.0)
#             cam_node = scene.add(camera, pose=pose)
#             color, _ = renderer.render(scene)
#             img = Image.fromarray(color)
#             img.save(os.path.join(output_dir, f"{basename}_{view_name}.png"))
#             print(f"🖼️ Saved {basename}_{view_name}.png")
#             scene.remove_node(cam_node)

#         renderer.delete()

#     except Exception as e:
#         print(f"❌ Failed to render {mesh_path}: {e}")

def render_views(mesh_path):
    try:
        scene_or_mesh = trimesh.load(mesh_path)

        # Convert scene to mesh if needed
        if isinstance(scene_or_mesh, trimesh.Scene):
            print(f"📦 Converting scene to mesh for {os.path.basename(mesh_path)}")
            combined = trimesh.util.concatenate([geometry for geometry in scene_or_mesh.dump()])
        elif isinstance(scene_or_mesh, list):
            combined = trimesh.util.concatenate(scene_or_mesh)
        else:
            combined = scene_or_mesh

        # Normalize mesh position and scale
        combined.apply_translation(-combined.centroid)
        combined.apply_scale(1.0 / max(combined.extents))

        # Convert to pyrender mesh
        mesh = pyrender.Mesh.from_trimesh(combined, smooth=False)

        # Create scene
        scene = pyrender.Scene()
        scene.add(mesh)

        # Add lights
        light = pyrender.DirectionalLight(color=np.ones(3), intensity=3.0)
        scene.add(light, pose=np.eye(4))

        # Renderer
        renderer = pyrender.OffscreenRenderer(viewport_width=768, viewport_height=768)

        # Camera poses based on normalized size
        camera_poses = {
            "front": trimesh.transformations.translation_matrix([0, 0, 2.5]),
            "top": trimesh.transformations.rotation_matrix(np.radians(90), [1, 0, 0]) @ trimesh.transformations.translation_matrix([0, 0, 2.5]),
            "isometric": trimesh.transformations.rotation_matrix(np.radians(35), [1, 0, 0]) @
                         trimesh.transformations.rotation_matrix(np.radians(45), [0, 1, 0]) @
                         trimesh.transformations.translation_matrix([0, 0, 2.5])
        }

        basename = os.path.splitext(os.path.basename(mesh_path))[0]

        for view_name, pose in camera_poses.items():
            camera = pyrender.PerspectiveCamera(yfov=np.pi / 3.0)
            cam_node = scene.add(camera, pose=pose)
            color, _ = renderer.render(scene)
            img = Image.fromarray(color)
            img.save(os.path.join(output_dir, f"{basename}_{view_name}.png"))
            print(f"🖼️ Saved {basename}_{view_name}.png")
            scene.remove_node(cam_node)

        renderer.delete()

    except Exception as e:
        print(f"❌ Failed to render {mesh_path}: {e}")


