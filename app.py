import os
import random
from flask import Flask, request, jsonify, render_template
from PIL import Image
import io
import tensorflow as tf  # Or your ML library of choice

app = Flask(__name__)

# Load your pre-trained model here, uncomment this line if you have a model
# model = tf.keras.models.load_model('path_to_your_model')

# Function to preprocess the uploaded image for the model
def preprocess_image(image):
    img = image.resize((224, 224))  # Adjust size as needed
    img = tf.keras.preprocessing.image.img_to_array(img)
    img = img / 255.0  # Normalize if needed
    img = img.reshape(1, 224, 224, 3)  # Assuming the model needs this input shape
    return img

# Route for rendering the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Route for handling image upload and prediction
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    try:
        # Load the image
        image = Image.open(io.BytesIO(file.read()))
    except Exception as e:
        return jsonify({'error': f'Failed to process image: {str(e)}'}), 400

    # Mock prediction for testing purposes
    labels = ['cat', 'dog', 'bird']
    prediction = random.choice(labels)

    return jsonify({'prediction': prediction})

if __name__ == '__main__':
    app.run(debug=True)
