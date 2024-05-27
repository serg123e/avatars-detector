# User avatars' scoring service

## Installation

  1. git clone https://github.com/serg123e/avatars-detector.git
  2. cd avatars-detector
  3. docker build -t avatars-detector .
  4. docker run -p 5080:80 avatars-detector

You can disable loading of some models to save memory and CPU:
      
    docker run -e ENABLE_NUDE=false -e ENABLE_NSFW=false -p 5080:80 avatars-detector

You can disable loading of some models to save memory and CPU:
      
    docker run -e ENABLE_CELEB=false -e ENABLE_NUDE=false -e ENABLE_NSFW=false -p 5080:80 avatars-detector


## Usage

Check [examples](examples)


## Training

Check [training](training)
  