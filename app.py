import os, subprocess, tempfile
from flask import Flask, request, send_file

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return {"error": "Dosya bulunamadi"}, 400
    
    file = request.files['file']
    
    with tempfile.TemporaryDirectory() as tmpdir:
        input_png = os.path.join(tmpdir, "input.png")
        output_mp4 = os.path.join(tmpdir, "output.mp4")
        
        file.save(input_png)
        
        cmd = [
            "ffmpeg", "-y", "-loop", "1", "-i", input_png,
            "-t", "5",
            "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,format=yuv420p",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", output_mp4
        ]
        
        subprocess.run(cmd, check=True)
        return send_file(output_mp4, mimetype='video/mp4')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)