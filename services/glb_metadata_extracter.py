# import os
# import json
# import numpy as np
# import trimesh

# def extract_glb_metadata(glb_path):
#     mesh = trimesh.load(glb_path)
#     if not isinstance(mesh, trimesh.Trimesh):
#         raise ValueError("Not a Trimesh object")

#     bbox = mesh.bounding_box.bounds
#     dims = bbox[1] - bbox[0]
#     volume = mesh.volume
#     surface_area = mesh.area
#     com = mesh.center_mass
#     inertia = mesh.moment_inertia

#     return {
#         "length": round(dims[0], 3),
#         "width": round(dims[1], 3),
#         "height": round(dims[2], 3),
#         "bounding_box": {
#             "xmin": round(bbox[0][0], 3), "xmax": round(bbox[1][0], 3),
#             "ymin": round(bbox[0][1], 3), "ymax": round(bbox[1][1], 3),
#             "zmin": round(bbox[0][2], 3), "zmax": round(bbox[1][2], 3)
#         },
#         "volume": round(volume, 3),
#         "surface_area": round(surface_area, 3),
#         "center_of_mass": {
#             "x": round(com[0], 3),
#             "y": round(com[1], 3),
#             "z": round(com[2], 3)
#         },
#         "inertia_tensor": np.round(inertia, 6).tolist()
#     }

# def main():
#     input_dir = "glb_files"
#     output_dir = "output_metadata"
#     os.makedirs(output_dir, exist_ok=True)

#     for fname in os.listdir(input_dir):
#         if fname.lower().endswith(".glb"):
#             try:
#                 print(f"Processing {fname}")
#                 meta = extract_glb_metadata(os.path.join(input_dir, fname))
#                 out_path = os.path.join(output_dir, fname.rsplit(".", 1)[0] + ".json")
#                 with open(out_path, "w") as f:
#                     json.dump(meta, f, indent=4)
#                 print(f"✅ Saved: {out_path}")
#             except Exception as e:
#                 print(f"❌ Error with {fname}: {e}")

# if __name__ == "__main__":
#     main()


import os
import json
import numpy as np
import trimesh

def extract_glb_metadata(glb_path):
    loaded = trimesh.load(glb_path)

    # If it's a Scene, concatenate all geometries
    if isinstance(loaded, trimesh.Scene):
        if not loaded.geometry:
            raise ValueError("GLB scene has no geometry.")
        mesh = trimesh.util.concatenate(tuple(loaded.geometry.values()))
    elif isinstance(loaded, trimesh.Trimesh):
        mesh = loaded
    else:
        raise ValueError("Unsupported GLB content type.")

    bbox = mesh.bounding_box.bounds
    dims = bbox[1] - bbox[0]
    volume = mesh.volume
    surface_area = mesh.area
    com = mesh.center_mass
    inertia = mesh.moment_inertia

    return {
        "length": round(dims[0], 3),
        "width": round(dims[1], 3),
        "height": round(dims[2], 3),
        "bounding_box": {
            "xmin": round(bbox[0][0], 3), "xmax": round(bbox[1][0], 3),
            "ymin": round(bbox[0][1], 3), "ymax": round(bbox[1][1], 3),
            "zmin": round(bbox[0][2], 3), "zmax": round(bbox[1][2], 3)
        },
        "volume": round(volume, 3),
        "surface_area": round(surface_area, 3),
        "center_of_mass": {
            "x": round(com[0], 3),
            "y": round(com[1], 3),
            "z": round(com[2], 3)
        },
        "inertia_tensor": np.round(inertia, 6).tolist()
    }

def main():
    input_dir = "glb_files"
    output_dir = "output_metadata"
    os.makedirs(output_dir, exist_ok=True)

    for fname in os.listdir(input_dir):
        if fname.lower().endswith(".glb"):
            path = os.path.join(input_dir, fname)
            try:
                print(f"Processing {fname}")
                meta = extract_glb_metadata(path)
                outpath = os.path.join(output_dir, fname.rsplit(".", 1)[0] + ".json")
                with open(outpath, "w") as f:
                    json.dump(meta, f, indent=4)
                print(f"✅ Saved: {outpath}")
            except Exception as e:
                print(f"❌ Error with {fname}: {e}")

if __name__ == "__main__":
    main()
