import os
import pathlib
from flask import Flask, request, jsonify
from PIL import Image
from flask_cors import CORS

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

# Environment variables to enable/disable models
ENABLE_RESNET = os.getenv('ENABLE_RESNET', 'true').lower() == 'true'
ENABLE_NSFW = os.getenv('ENABLE_NSFW', 'true').lower() == 'true'
ENABLE_NUDE = os.getenv('ENABLE_NUDE', 'true').lower() == 'true'
ENABLE_CELEB = os.getenv('ENABLE_CELEB', 'true').lower() == 'true'

file_path = pathlib.Path(__file__).parent.absolute()

if ENABLE_NSFW:
    import nsfw_predict
    NSFW_MODEL_PATH = f'{file_path}/models/nsfw_mobilenet2.224x224.h5'
    nsfw_model = nsfw_predict.load_model(NSFW_MODEL_PATH)

if ENABLE_NUDE:
    from nudenet import NudeDetector
    nude_detector = NudeDetector()

if ENABLE_CELEB:
    from celeb_detector import celeb_recognition

if ENABLE_RESNET:
    import avatar_detector
    # from avatar_detector import classify as classify_avatar
    RESNET_MODEL_PATH = f'{file_path}/models/resnet_model95.69.pth'
    resnet_model = avatar_detector.load_model(RESNET_MODEL_PATH)


app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    if file:
        temp_path = os.path.join('/tmp', file.filename)
        file.save(temp_path)

        response = {}

        # Process the image for classification
        if ENABLE_RESNET:
            image = Image.open(temp_path).convert('RGB')
            classification_result = avatar_detector.classify(resnet_model, image)
            response['avatar_classification'] = classification_result

        # Predict single image
        if ENABLE_NSFW:
            nsfw_results = nsfw_predict.classify_one(nsfw_model, temp_path)
            response['nsfw_model'] = nsfw_results

        # Use NudeDetector on the saved file
        if ENABLE_NUDE:
            nudity_results = nude_detector.detect(temp_path)
            response['nudenet'] = nudity_results

        # Run celebrity detector
        if ENABLE_CELEB:
            celeb_detector_results = celeb_recognition.get_celebrity(temp_path)
            response['celeb_detector'] = celeb_detector_results

        # Optionally remove the file if you no longer need it
        os.remove(temp_path)

        return jsonify(response)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5080)
