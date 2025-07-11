# from OCC.Core.IGESControl import IGESControl_Reader
# from OCC.Display.SimpleGui import init_display

# # Replace with your full IGES file path if needed
# iges_path = "851_4-700-t3l-st.igs"

# reader = IGESControl_Reader()
# status = reader.ReadFile(iges_path)

# if status == 1:
#     reader.TransferRoots()
#     shape = reader.OneShape()

#     display, start_display, _, _ = init_display()
#     display.DisplayShape(shape, update=True)
#     start_display()
# else:
#     print("Failed to read IGES file.")

from OCC.Core.IGESControl import IGESControl_Reader
from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.BRep import BRep_Tool
from OCC.Core.TopoDS import topods

from OCC.Core.TopAbs import TopAbs_FACE
from OCC.Core.BRep import BRep_Tool
from OCC.Display.SimpleGui import init_display

import numpy as np

def extract_points_from_shape(shape, linear_deflection=0.1, angular_deflection=0.1):
    # Mesh the shape
    mesh = BRepMesh_IncrementalMesh(shape, linear_deflection, False, angular_deflection, True)
    mesh.Perform()

    points = []
    exp = TopExp_Explorer(shape, TopAbs_FACE)
    while exp.More():
        face = topods.Face(exp.Current())
        location = face.Location()
        triangulation = BRep_Tool.Triangulation(face, location)
        if triangulation:
            for i in range(1, triangulation.NbNodes() + 1):
                p = triangulation.Node(i)
                points.append([p.X(), p.Y(), p.Z()])
        exp.Next()
    return np.array(points)

# Load IGES file
iges_path = "z45w_abs.igs"
filename="z45w_abs"
reader = IGESControl_Reader()
status = reader.ReadFile(iges_path)

if status == 1:
    reader.TransferRoots()
    shape = reader.OneShape()

    # Show the model
    display, start_display, _, _ = init_display()
    display.DisplayShape(shape, update=True)

    # Extract point cloud
    point_cloud = extract_points_from_shape(shape)
    print(f"\nExtracted {len(point_cloud)} surface points.")
    
    # Save point cloud as CSV (optional)
    np.savetxt(f"{filename}_point_cloud.csv", point_cloud, delimiter=",", header="x,y,z", comments="")
    print("Point cloud saved to 'point_cloud.csv'.")
    
    start_display()
else:
    print("Failed to read IGES file.")
