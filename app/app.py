import os
import pathlib
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.security.api_key import APIKeyHeader
from PIL import Image
from fastapi.middleware.cors import CORSMiddleware
import shutil

API_TOKEN = os.getenv("API_TOKEN")
api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

if API_TOKEN:
  print("API_TOKEN specified, authorization enabled") 
else:
  print("API_TOKEN not specified, authorization DISABLED. Do not expose the service to public")

file_path = pathlib.Path(__file__).parent.absolute()

AVATAR_MODEL_PATH = os.getenv("AVATAR_MODEL_PATH", f'{file_path}/models/resnet_model91.81.pth')
NSFW_MODEL_PATH = os.getenv("NSFW_MODEL_PATH", f'{file_path}/models/nsfw_mobilenet2.224x224.h5')

# Environment variables to enable/disable models
AVATAR_DETECTOR = os.getenv('AVATAR_DETECTOR', 'true').lower() == 'true'
NSFW_DETECTOR = os.getenv('NSFW_DETECTOR', 'true').lower() == 'true'
NUDE_DETECTOR = os.getenv('NUDE_DETECTOR', 'true').lower() == 'true'

if NSFW_DETECTOR:
    import nsfw_predict
    nsfw_model = nsfw_predict.load_model(NSFW_MODEL_PATH)
    print("Loaded: nsfw_predict")

if NUDE_DETECTOR:
    from nudenet import NudeDetector
    nude_detector = NudeDetector()
    print("Loaded: nude_detector")

if AVATAR_DETECTOR:
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

def get_api_key(api_key_header: str = Depends(api_key_header)):
    if API_TOKEN and api_key_header != API_TOKEN:

        raise HTTPException(status_code=403, detail=f"Could not validate credentials")
    return api_key_header

@app.post("/upload")
async def upload_file(file: UploadFile = File(...), api_key: str = Depends(get_api_key)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No selected file")

    temp_path = os.path.join('/tmp', file.filename)

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    response = {}

    # Process the image for classification
    if AVATAR_DETECTOR:
        image = Image.open(temp_path).convert('RGB')
        classification_result = avatar_detector.classify(resnet_model, image)
        response['avatar_detector'] = classification_result

    # Predict single image
    if NSFW_DETECTOR:
        nsfw_results = nsfw_predict.classify_one(nsfw_model, temp_path)
        response['nsfw_model'] = nsfw_results

    # Use NudeDetector on the saved file
    if NUDE_DETECTOR:
        nudity_results = nude_detector.detect(temp_path)
        response['nudenet'] = nudity_results

    # Optionally remove the file if you no longer need it
    os.remove(temp_path)

    return JSONResponse(content=response)

@app.get("/", response_class=HTMLResponse)
async def get_form():
    html_content = """
        <h1>Upload File to Avatar Detector</h1>
        <form action="/upload" enctype="multipart/form-data" method="post">
            <input name="file" type="file">
            <input type="submit">
        </form>
    """
    return HTMLResponse(content=html_content)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=80)