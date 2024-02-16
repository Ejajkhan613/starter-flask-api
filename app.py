from flask import Flask, request, jsonify, send_file
import os
import requests
import rembg
from io import BytesIO
from PIL import Image

app = Flask(__name__)

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

		# Save processed image temporarily or send it directly to the frontend
		# Here, we are converting it back to bytes and sending it as a response
		output_buffer = BytesIO()
		output_image.save(output_buffer, format="PNG")
		output_buffer.seek(0)

		# Create a response with the processed image
		return send_file(output_buffer, mimetype='image/png')
