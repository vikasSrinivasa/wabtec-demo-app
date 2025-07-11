import os
from OCC.Extend.DataExchange import read_iges_file
from OCC.Display.OCCViewer import rgb_color
from OCC.Display.SimpleGui import init_display

def render_iges_to_images(iges_file_path, output_dir):
    shapes = read_iges_file(iges_file_path)
    if not shapes:
        raise ValueError("No shapes found in file.")
    shape = shapes[0]
    if shape.IsNull():
        raise ValueError("Loaded shape is null.")

    display, start_display, _, _ = init_display()
    display.DisplayShape(shape, update=True)
    display.View.SetBackgroundColor(rgb_color(1.0, 1.0, 1.0))  # white background

    base_name = os.path.splitext(os.path.basename(iges_file_path))[0]
    os.makedirs(output_dir, exist_ok=True)

    # Isometric
    display.View_Iso()
    display.FitAll()
    display.View.Dump(os.path.join(output_dir, f"{base_name}_isometric.png"))

    # Top
    display.View_Top()
    display.FitAll()
    display.View.Dump(os.path.join(output_dir, f"{base_name}_top.png"))

    # Front
    display.View_Front()
    display.FitAll()
    display.View.Dump(os.path.join(output_dir, f"{base_name}_front.png"))

    display.EraseAll()

if __name__ == "__main__":
    INPUT_DIR = "iges_files"
    OUTPUT_DIR = "rendered_images"
    for file in os.listdir(INPUT_DIR):
        if file.lower().endswith((".igs", ".iges")):
            input_path = os.path.join(INPUT_DIR, file)
            print(f"📦 Rendering {file}...")
            try:
                render_iges_to_images(input_path, OUTPUT_DIR)
                print(f"✅ Done: {file}")
            except Exception as e:
                print(f"❌ Failed to render {file}: {e}")
