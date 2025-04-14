import os
from flask import Flask, render_template, request, send_from_directory
import subprocess

app = Flask(__name__)

# Paths
UPLOAD_FOLDER = 'static/uploads'
MODEL_FOLDER = 'static/models'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MODEL_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return "No image uploaded", 400
    image = request.files['image']
    if image.filename == '':
        return "No selected file", 400
    image_path = os.path.join(UPLOAD_FOLDER, image.filename)
    image.save(image_path)

    # Run TripoSR with the uploaded image
    cmd = f"python3 TripoSR/run.py {image_path}"
    # cmd = f"python3 TripoSR/run.py {image_path} --bake-texture --render"
    subprocess.run(cmd, shell=True)

    return {"model": image.filename.replace('.png', '.obj')}

@app.route('/modify_model', methods=['POST'])
def modify_model():
    prompt = request.form['prompt']
    model_path = request.form['model_path']

    if prompt:
        # Run Text2Mesh with the given prompt
        cmd = f"python3 text2mesh/main.py --input {MODEL_FOLDER}/{model_path} --prompt '{prompt}'"
        subprocess.run(cmd, shell=True)

    return {"status": "modified"}

@app.route('/download_model/<filename>')
def download_model(filename):
    return send_from_directory(MODEL_FOLDER, filename)

@app.route('/get_model/<filename>')
def get_model(filename):
    return send_from_directory(MODEL_FOLDER, filename)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
