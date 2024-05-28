# User avatars' scoring service

## Installation

  1. clone repository
  2. docker build -t avatars-detector .
  3. docker run -e ENABLE_CELEB=false -e ENABLE_NUDE=false -e ENABLE_NSFW=false -p 5080:80 avatars-detector


## Usage

  check [examples](examples)


## Training
  