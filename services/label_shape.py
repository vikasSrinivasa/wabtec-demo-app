import base64, os, json, time
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # API key pulled from env

IMAGE_DIR = Path("rendered_images")
METADATA_DIR = Path("metadata")
OUTPUT_DIR = Path("labels")
OUTPUT_DIR.mkdir(exist_ok=True)

def generate_gpt_labels():
    start = time.time()
    results = []
    metadata_files = list(METADATA_DIR.glob("*.json"))

    for metadata_file in metadata_files:
        model_name = metadata_file.stem
        output_file = OUTPUT_DIR / f"{model_name}_label.json"

        # Skip if already labeled
        if output_file.exists():
            continue

        try:
            metadata_dict = json.loads(metadata_file.read_text())
            metadata_str = json.dumps(metadata_dict, indent=2)
        except Exception as e:
            results.append({"model": model_name, "status": "failed", "error": f"JSON read error: {e}"})
            continue

        # Load all 3 views
        view_paths = [
            IMAGE_DIR / f"{model_name}_front.png",
            IMAGE_DIR / f"{model_name}_top.png",
            IMAGE_DIR / f"{model_name}_isometric.png"
        ]

        images_content = []
        missing = False

        for path in view_paths:
            if not path.exists():
                results.append({"model": model_name, "status": "skipped", "error": f"Missing image: {path.name}"})
                missing = True
                break

            img_bytes = path.read_bytes()
            img_base64 = base64.b64encode(img_bytes).decode()
            images_content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{img_base64}"
                }
            })

        if missing:
            continue

        # GPT Vision Prompt
        prompt = f"""
You are given a mechanical part's raw metadata and 3 rendered images (front, top, and isometric views).

🔧 Metadata (in raw JSON form):
{metadata_str}

📷 Use the images and metadata together to answer:

1. Provide a **short semantic label** for this part (e.g., "bore clamp", "gearbox housing", "engine block").
2. Provide a **1–2 line description** of its function or use in mechanical assemblies.
"""

        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{
                    "role": "user",
                    "content": [{"type": "text", "text": prompt}, *images_content]
                }],
                temperature=0.2
            )

            label = response.choices[0].message.content.strip()
            data = {
                "model": model_name,
                "label": label,
                "geometry": metadata_dict
            }

            with open(output_file, "w") as f:
                json.dump(data, f, indent=2)

            results.append({"model": model_name, "status": "success", "label": label.split('\n')[0]})

        except Exception as e:
            results.append({"model": model_name, "status": "failed", "error": str(e)})

    elapsed = round(time.time() - start, 2)
    return {
        "summary": {
            "processed": len(results),
            "time_seconds": elapsed
        },
        "results": results
    }
