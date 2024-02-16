from flask import Flask, request, jsonify
import os
import requests
import rembg
from io import BytesIO
from PIL import Image

app = Flask(__name__)

# Define the path to the uploads folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def hello_world():
    return 'Hello, world!'

@app.route('/process_image', methods=['POST'])
def process_image():
    # Get image file from frontend
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image_file = request.files['image']

    # Read image and process it using rembg
    image_bytes = image_file.read()
    output_bytes = rembg.remove(image_bytes)

    # Convert output bytes to image
    output_image = Image.open(BytesIO(output_bytes))

    # Save processed image to uploads folder
    filename = secure_filename(image_file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    output_image.save(filepath)

    # Generate URL for the saved image
    image_url = request.url_root + os.path.join(app.config['UPLOAD_FOLDER'], filename)

    # Return success response with image URL
    return jsonify({'message': 'Image processed successfully', 'image_url': image_url}), 200
