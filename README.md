# User avatars' scoring service

## Run from Docker Hub

    docker run -p 5080:80 -e API_TOKEN=your_api_token serg123e/avatars-detector:latest

## Build local image and run

  1. git lfs install
  2. git clone https://github.com/serg123e/avatars-detector.git
  3. cd avatars-detector
  4. docker build -t avatars-detector .
  5. docker run -p 5080:80 -e API_TOKEN=your_api_token avatars-detector

You can disable loading of some models to save memory and CPU:
      
    docker run -e NUDE_DETECTOR=false -e NSFW_DETECTOR=false -p 5080:80 avatars-detector

## Authentication

    curl -X POST "http://localhost:5080/upload" -H "Authorization: your_api_token" -F "file=@./path/to/your/file.jpg"

  If the environment variable API_TOKEN is not set, you can simply use:

    curl -X POST "http://localhost:5080/upload" -F "file=@./path/to/your/file.jpg"

## Usage

Check [examples](examples)

## Training

Check [training](training)
  
## Example response

```json
{
    "avatar_detector":
    {
        "good": 0.9437850713729858,
        "bad": 0.056214939802885056
    },
    "nsfw_model":
    {
        "drawings": 0.000020054891137988307,
        "hentai": 0.0000011956053640460595,
        "neutral": 0.9998780488967896,
        "porn": 0.00005732426870963536,
        "sexy": 0.0000434463654528372
    },
    "nudenet":
    [
        {
            "class": "FACE_FEMALE",
            "score": 0.7747942805290222,
            "box":
            [
                523,
                359,
                297,
                302
            ]
        }
    ]
}
```
