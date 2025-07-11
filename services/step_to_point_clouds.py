import os
import csv
import numpy as np
from OCC.Extend.DataExchange import read_step_file
from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_FACE
from OCC.Core.TopoDS import topods
from OCC.Core.BRep import BRep_Tool

# Paths
INPUT_DIR = "step_files"
OUTPUT_DIR = "step_point_clouds"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_points_from_shape(shape, linear_deflection=0.1, angular_deflection=0.1):
    mesh = BRepMesh_IncrementalMesh(shape, linear_deflection, False, angular_deflection, True)
    mesh.Perform()

    points = []
    exp = TopExp_Explorer(shape, TopAbs_FACE)
    while exp.More():
        face = topods.Face(exp.Current())
        triangulation = BRep_Tool.Triangulation(face, face.Location())
        if triangulation:
            for i in range(1, triangulation.NbNodes() + 1):
                p = triangulation.Node(i)
                points.append([p.X(), p.Y(), p.Z()])
        exp.Next()
    return np.array(points)

def main():
    for fname in os.listdir(INPUT_DIR):
        if not fname.lower().endswith((".step", ".stp")):
            continue
        try:
            print(f"📦 Processing: {fname}")
            path = os.path.join(INPUT_DIR, fname)
            shape = read_step_file(path)
            if shape.IsNull():
                print(f"❌ Skipped {fname} (null shape)")
                continue
            points = extract_points_from_shape(shape)
            if points.shape[0] == 0:
                print(f"⚠️ No points found in {fname}")
                continue
            csv_path = os.path.join(OUTPUT_DIR, fname.rsplit(".", 1)[0] + "_point_cloud.csv")
            np.savetxt(csv_path, points, delimiter=",", header="x,y,z", comments="")
            print(f"✅ Saved: {csv_path}")
        except Exception as e:
            print(f"❌ Failed for {fname}: {e}")

if __name__ == "__main__":
    main()
