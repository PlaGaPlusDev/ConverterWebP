from flask import Flask, render_template, request, send_from_directory, jsonify
import os
from converter import convert_image

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'converted'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No image file selected'}), 400

    output_format = request.form.get('output_format', 'png')
    compression = int(request.form.get('compression', 95))
    fps = int(request.form.get('fps', 24))

    # Save the uploaded file temporarily
    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(input_path)

    # Convert the image
    success, result_msg = convert_image(
        input_path=input_path,
        output_dir=OUTPUT_FOLDER,
        output_format=output_format,
        compression=compression,
        fps=fps
    )

    if success:
        base_name = os.path.splitext(file.filename)[0]
        output_filename = f"{base_name}.{output_format}"
        return jsonify({'download_url': f'/download/{output_filename}'})
    else:
        return jsonify({'error': f'Error during conversion: {result_msg}'}), 500

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(OUTPUT_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
