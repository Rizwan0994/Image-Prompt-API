from flask import Flask, request, jsonify
from PIL import Image
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

@app.route('/predict_caption', methods=['POST'])
def predict_caption():
    img_data = request.files.get('image_data')
    text = "a photography of"

    image = Image.open(img_data).convert('RGB')

    inputs = processor(image, text, return_tensors="pt")
    output = model.generate(**inputs)
    caption = processor.decode(output[0], skip_special_tokens=True)
    return jsonify({'caption': caption})

@app.route('/test', methods=['GET'])
def test_endpoint():
    return "Testing App"

# This block ensures the app runs only when executed directly, not when imported as a module
if __name__ == '__main__':
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    app.run(host=host, port=port)
