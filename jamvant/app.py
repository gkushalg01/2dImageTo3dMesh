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
    command = f"source ../TripoSR/venv/bin/activate && python3 ../TripoSR/run.py {image_path} --output-dir {MODEL_FOLDER} --device=\"cpu\""
    process = subprocess.Popen(
        ["/bin/bash", "-c", command],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
    )

    for line in process.stdout:
        print("[img2mesh]", line.strip())

    process.wait()
    if process.returncode != 0:
        raise RuntimeError("TripoSR inference failed.")
    
    return {"model": "0/mesh.obj"}

@app.route('/modify_model', methods=['POST'])
def modify_model():
    prompt = request.form['prompt']

    if prompt:
        # Run Text2Mesh with the given prompt 
        txtcmd = f"python ../text2mesh/main.py --run branch --obj_path {MODEL_FOLDER}/0/mesh.obj --output_dir results/demo/output --prompt {prompt} --sigma 5.0  --clamp tanh --n_normaugs 4 --n_augs 1 --normmincrop 0.1 --normmaxcrop 0.1 --geoloss --colordepth 2 --normdepth 2 --frontview --frontview_std 4 --clipavg view --lr_decay 0.9 --clamp tanh --normclamp tanh  --maxcrop 1.0 --save_render --seed 41 --n_iter 1500 --background 1 1 1 "
        # txtcmd = f"python ../text2mesh/main.py --run branch --obj_path {MODEL_FOLDER}/0/mesh.obj --output_dir results/demo/output --prompt {prompt}"
        command = f"conda run -n text2mesh {txtcmd}"
        process = subprocess.Popen(
            ["/bin/bash", "-c", command],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
        )

        for line in process.stdout:
            print("[Text2Mesh]", line.strip())

        process.wait()
        if process.returncode != 0:
            raise RuntimeError("Text2Mesh prompt editing failed.")
        
        print("Text2Mesh finished successfully.")

    return {"status": "modified"}

@app.route('/download_model/<path:filename>')
def download_model(filename):
    return send_from_directory(MODEL_FOLDER, filename)

@app.route('/get_model/<path:filename>')
def get_model(filename):
    return send_from_directory(MODEL_FOLDER, filename)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
