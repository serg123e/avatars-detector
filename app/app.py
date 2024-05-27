import os
import pathlib
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
from fastapi.middleware.cors import CORSMiddleware
import shutil

file_path = pathlib.Path(__file__).parent.absolute()

AVATAR_MODEL_PATH = f'{file_path}/models/resnet_model91.81.pth'
NSFW_MODEL_PATH = f'{file_path}/models/nsfw_mobilenet2.224x224.h5'

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

# Environment variables to enable/disable models
ENABLE_AVATAR = os.getenv('ENABLE_AVATAR', 'true').lower() == 'true'
ENABLE_NSFW = os.getenv('ENABLE_NSFW', 'true').lower() == 'true'
ENABLE_NUDE = os.getenv('ENABLE_NUDE', 'true').lower() == 'true'

if ENABLE_NSFW:
    import nsfw_predict
    nsfw_model = nsfw_predict.load_model(NSFW_MODEL_PATH)
    print("Loaded: nsfw_predict")

if ENABLE_NUDE:
    from nudenet import NudeDetector
    nude_detector = NudeDetector()
    print("Loaded: nude_detector")

if ENABLE_AVATAR:
    import avatar_detector
    # from avatar_detector import classify as classify_avatar
    resnet_model = avatar_detector.load_model(AVATAR_MODEL_PATH)
    print("Loaded: avatar_detector")

app = FastAPI()

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No selected file")

    temp_path = os.path.join('/tmp', file.filename)

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    response = {}

    # Process the image for classification
    if ENABLE_AVATAR:
        image = Image.open(temp_path).convert('RGB')
        classification_result = avatar_detector.classify(resnet_model, image)
        response['avatar_detector'] = classification_result

    # Predict single image
    if ENABLE_NSFW:
        nsfw_results = nsfw_predict.classify_one(nsfw_model, temp_path)
        response['nsfw_model'] = nsfw_results

    # Use NudeDetector on the saved file
    if ENABLE_NUDE:
        nudity_results = nude_detector.detect(temp_path)
        response['nudenet'] = nudity_results

    # Optionally remove the file if you no longer need it
    os.remove(temp_path)

    return JSONResponse(content=response)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=80)