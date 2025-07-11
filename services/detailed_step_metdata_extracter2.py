import os
import json
from OCC.Extend.DataExchange import read_step_file
from OCC.Extend.ShapeFactory import get_boundingbox
from OCC.Core.TopAbs import TopAbs_FACE, TopAbs_EDGE, TopAbs_VERTEX, TopAbs_SHELL
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.BRepGProp import (
    brepgprop_VolumeProperties,
    brepgprop_SurfaceProperties
)
from OCC.Core.GProp import GProp_GProps
from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh
from OCC.Core.BRepClass3d import BRepClass3d_SolidClassifier
from OCC.Core.gp import gp_Pnt

def count_topo_elements(shape, topo_type):
    exp = TopExp_Explorer(shape, topo_type)
    count = 0
    while exp.More():
        count += 1
        exp.Next()
    return count

def extract_metadata(file_path):
    shape = read_step_file(file_path)
    if shape.IsNull():
        raise ValueError("Shape is null.")

    BRepMesh_IncrementalMesh(shape, 0.1).Perform()

    xmin, ymin, zmin, xmax, ymax, zmax = get_boundingbox(shape)
    length, width, height = xmax - xmin, ymax - ymin, zmax - zmin
    bbox_center = gp_Pnt((xmin + xmax)/2, (ymin + ymax)/2, (zmin + zmax)/2)

    # Volume + inertia
    volume_props = GProp_GProps()
    brepgprop_VolumeProperties(shape, volume_props)
    volume = volume_props.Mass()
    com = volume_props.CentreOfMass()
    inertia = volume_props.MatrixOfInertia()

    # Surface area
    surface_props = GProp_GProps()
    brepgprop_SurfaceProperties(shape, surface_props)
    surface_area = surface_props.Mass()

    # Compactness
    compactness = (volume ** 2) / (surface_area ** 3) if surface_area > 0 else None

    # Radius of gyration
    try:
        rg = {
            "x": round((inertia.Value(1, 1) / volume) ** 0.5, 3),
            "y": round((inertia.Value(2, 2) / volume) ** 0.5, 3),
            "z": round((inertia.Value(3, 3) / volume) ** 0.5, 3)
        }
    except:
        rg = None

    # Projected areas
    projections = {
        "XY": round(length * width, 3),
        "YZ": round(width * height, 3),
        "XZ": round(length * height, 3)
    }

    # Bounding sphere radius
    radius = round((((length ** 2 + width ** 2 + height ** 2) ** 0.5) / 2), 3)

    # Closed solid check
    classifier = BRepClass3d_SolidClassifier(shape)
    classifier.Perform(bbox_center, 1e-6)
    is_closed = classifier.State() == 0  # TopAbs_IN

    return {
        "length": round(length, 3),
        "width": round(width, 3),
        "height": round(height, 3),
        "bounding_box": {
            "xmin": round(xmin, 3), "xmax": round(xmax, 3),
            "ymin": round(ymin, 3), "ymax": round(ymax, 3),
            "zmin": round(zmin, 3), "zmax": round(zmax, 3)
        },
        "volume": round(volume, 3),
        "center_of_mass": {
            "x": round(com.X(), 3),
            "y": round(com.Y(), 3),
            "z": round(com.Z(), 3)
        },
        "surface_area": round(surface_area, 3),
        "compactness": round(compactness, 6) if compactness else None,
        "inertia_tensor": {
            "ixx": round(inertia.Value(1, 1), 6),
            "iyy": round(inertia.Value(2, 2), 6),
            "izz": round(inertia.Value(3, 3), 6),
            "ixy": round(inertia.Value(1, 2), 6),
            "ixz": round(inertia.Value(1, 3), 6),
            "iyz": round(inertia.Value(2, 3), 6)
        },
        "radius_of_gyration": rg,
        "projected_area": projections,
        "bounding_sphere_radius": radius,
        "face_count": count_topo_elements(shape, TopAbs_FACE),
        "edge_count": count_topo_elements(shape, TopAbs_EDGE),
        "vertex_count": count_topo_elements(shape, TopAbs_VERTEX),
        "shell_count": count_topo_elements(shape, TopAbs_SHELL),
        "is_closed_solid": is_closed
    }

def main():
    INPUT_DIR = "step_files"
    OUTPUT_DIR = "output_metadata"
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for filename in os.listdir(INPUT_DIR):
        if filename.lower().endswith((".step", ".stp")):
            file_path = os.path.join(INPUT_DIR, filename)
            try:
                print(f"Processing {filename}...")
                meta = extract_metadata(file_path)
                out_path = os.path.join(OUTPUT_DIR, filename.replace(".step", ".json").replace(".stp", ".json"))
                with open(out_path, "w") as f:
                    json.dump(meta, f, indent=4)
                print(f"✅ Saved: {out_path}")
            except Exception as e:
                print(f"❌ Error with {filename}: {e}")

if __name__ == "__main__":
    main()
