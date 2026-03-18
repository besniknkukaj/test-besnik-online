import os
import base64
import replicate
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

REPLICATE_API_TOKEN = os.environ.get("REPLICATE_API_TOKEN", "")

@app.route("/render", methods=["POST"])
def render():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    style = request.form.get("style", "modern")
    prompt_map = {
        "modern":    "ultra realistic modern architectural render, photorealistic, 8K, professional architectural visualization, clean lines, contemporary design, dramatic lighting, high detail",
        "luxury":    "ultra realistic luxury villa architectural render, photorealistic, 8K, elegant design, marble, glass, dramatic sunset lighting, professional CGI",
        "minimalist":"ultra realistic minimalist architectural render, photorealistic, 8K, white walls, natural light, Scandinavian design, professional visualization",
        "classic":   "ultra realistic classic architectural render, photorealistic, 8K, traditional architecture, stone facade, warm lighting, professional CGI render",
    }
    prompt = prompt_map.get(style, prompt_map["modern"])

    img_data = base64.b64encode(file.read()).decode("utf-8")
    mime = file.content_type or "image/jpeg"
    data_uri = f"data:{mime};base64,{img_data}"

    os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

    output = replicate.run(
        "black-forest-labs/flux-dev",
        input={
            "image": data_uri,
            "prompt": prompt,
            "prompt_strength": 0.75,
            "num_inference_steps": 50,
            "guidance": 3.5,
            "output_format": "jpg",
            "output_quality": 95,
        }
    )

    urls = list(output) if hasattr(output, "__iter__") else [output]
    return jsonify({"url": str(urls[0])})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
