
import os
from OCC.Extend.DataExchange import read_step_file
from OCC.Display.OCCViewer import rgb_color
from OCC.Display.SimpleGui import init_display

def render_step_to_images(step_file_path, output_dir):
    shape = read_step_file(step_file_path)

    if shape.IsNull():
        raise ValueError("Shape is null")

    display, start_display, _, _ = init_display()
    display.DisplayShape(shape, update=True)

    # ✅ Correct float RGB values for white background
    display.View.SetBackgroundColor(rgb_color(1.0, 1.0, 1.0))

    base_name = os.path.splitext(os.path.basename(step_file_path))[0]
    os.makedirs(output_dir, exist_ok=True)

    # Isometric View
    display.View_Iso()
    display.FitAll()
    display.View.Dump(os.path.join(output_dir, f"{base_name}_isometric.png"))

    # Top View
    display.View_Top()
    display.FitAll()
    display.View.Dump(os.path.join(output_dir, f"{base_name}_top.png"))

    # Front View
    display.View_Front()
    display.FitAll()
    display.View.Dump(os.path.join(output_dir, f"{base_name}_front.png"))

    display.EraseAll()

# Example usage
# if __name__ == "__main__":
#     INPUT_FILE = "step_files/E10112070.step"
#     OUTPUT_DIR = "rendered_images"
#     render_step_to_images(INPUT_FILE, OUTPUT_DIR)
if __name__ == "__main__":
    INPUT_DIR = "step_files"
    OUTPUT_DIR = "rendered_images"

    for file in os.listdir(INPUT_DIR):
        if file.lower().endswith(".step") or file.lower().endswith(".stp"):
            input_path = os.path.join(INPUT_DIR, file)
            print(f"📦 Rendering {file}...")
            try:
                render_step_to_images(input_path, OUTPUT_DIR)
                print(f"✅ Done: {file}")
            except Exception as e:
                print(f"❌ Failed to render {file}: {e}")
