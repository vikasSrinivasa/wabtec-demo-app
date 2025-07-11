# import os
# import numpy as np
# from pathlib import Path
# import trimesh
# from OCC.Extend.DataExchange import read_step_file, read_iges_file
# from step_to_point_clouds import extract_points_from_shape as extract_step_points
# from view_iges import extract_points_from_shape as extract_iges_points

# OUTPUT_DIR = Path("outputs")
# OUTPUT_DIR.mkdir(exist_ok=True)

# def convert_to_pointcloud(file_path: str) -> str:
#     path = Path(file_path)
#     ext = path.suffix.lower()
#     base_name = path.stem
#     out_csv = OUTPUT_DIR / f"{base_name}_point_cloud.csv"

#     if ext == ".glb":
#         mesh = trimesh.load(file_path)
#         if isinstance(mesh, trimesh.Scene):
#             mesh = mesh.dump()
#         if isinstance(mesh, list):
#             mesh = trimesh.util.concatenate(mesh)
#         if not isinstance(mesh, trimesh.Trimesh):
#             raise ValueError("❌ GLB could not be interpreted as a mesh.")
#         np.savetxt(out_csv, mesh.vertices, delimiter=",", header="x,y,z", comments="")

#     elif ext in [".step", ".stp"]:
#         shape = read_step_file(file_path)
#         if shape.IsNull():
#             raise ValueError("❌ STEP shape is null.")
#         points = extract_step_points(shape)
#         if points.shape[0] == 0:
#             raise ValueError("❌ No points found in STEP.")
#         np.savetxt(out_csv, points, delimiter=",", header="x,y,z", comments="")

#     elif ext in [".igs", ".iges"]:
#         shapes = read_iges_file(file_path)
#         if not shapes:
#             raise ValueError("❌ No shapes found in IGES.")
#         shape = shapes[0]  # Assume first
#         points = extract_iges_points(shape)
#         if points.shape[0] == 0:
#             raise ValueError("❌ No points found in IGES.")
#         np.savetxt(out_csv, points, delimiter=",", header="x,y,z", comments="")

#     else:
#         raise ValueError(f"Unsupported format: {ext}")

#     return str(out_csv)
from pathlib import Path
import numpy as np
import trimesh
from OCC.Extend.DataExchange import read_step_file, read_iges_file
from services.step_to_point_clouds import extract_points_from_shape as extract_step_points
from services.view_iges import extract_points_from_shape as extract_iges_points
import time 
POINTCLOUD_DIR = Path("point_clouds")
UPLOADS_DIR = Path("uploads")
POINTCLOUD_DIR.mkdir(exist_ok=True)

def process_all_files_to_pointclouds():
    start = time.time()
    results = []
    supported_exts = [".step", ".stp", ".igs", ".iges", ".glb"]

    for file_path in UPLOADS_DIR.glob("*"):
        ext = file_path.suffix.lower()
        if ext not in supported_exts:
            continue

        try:
            out_path = POINTCLOUD_DIR / f"{file_path.stem}_point_cloud.csv"

            if ext == ".glb":
                mesh = trimesh.load(file_path)
                if isinstance(mesh, trimesh.Scene):
                    mesh = mesh.dump()
                if isinstance(mesh, list):
                    mesh = trimesh.util.concatenate(mesh)
                if not isinstance(mesh, trimesh.Trimesh):
                    raise ValueError("GLB is not a mesh")
                np.savetxt(out_path, mesh.vertices, delimiter=",", header="x,y,z", comments="")

            elif ext in [".step", ".stp"]:
                shape = read_step_file(str(file_path))
                if shape.IsNull():
                    raise ValueError("STEP shape is null")
                points = extract_step_points(shape)
                np.savetxt(out_path, points, delimiter=",", header="x,y,z", comments="")

            elif ext in [".igs", ".iges"]:
                shapes = read_iges_file(str(file_path))
                if not shapes:
                    raise ValueError("No IGES shapes found")
                points = extract_iges_points(shapes[0])
                np.savetxt(out_path, points, delimiter=",", header="x,y,z", comments="")

            results.append({
                "file": file_path.name,
                "pointcloud_csv": str(out_path)
            })

        except Exception as e:
            results.append({
                "file": file_path.name,
                "error": str(e)
            })
    elapsed = round(time.time() - start, 2)
    return {
        "results": results,
        "elapsed_time": elapsed
    }
