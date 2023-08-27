from flask import Flask, request, jsonify
from PIL import Image
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Add CORS so that frontend can access backend API
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

@app.route('/predict_caption', methods=['POST'])
def predict_caption():
    img_data = request.files.get('image_data')  # Get image data from POST request
    text = "a photography of"  # You can customize the text
    
    # Convert FileStorage to PIL.Image.Image
    image = Image.open(img_data).convert('RGB')
    
    inputs = processor(image, text, return_tensors="pt")
    output = model.generate(**inputs)
    caption = processor.decode(output[0], skip_special_tokens=True)
    print(caption)
    return jsonify({'caption': caption})

@app.route('/test', methods=['GET'])
def test_endpoint():
    return "Testing App"

# This block ensures the app runs only when executed directly, not when imported as a module
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Run on all available network interfaces
