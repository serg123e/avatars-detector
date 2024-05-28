# How to train new model

  * install required libraries

        pip install -r training/requirements.txt

  * put training files to /content/avatars/good and /content/avatars/bad folders:

        tar zxf archive_with_avatars.tgz -C /content/avatars/

 * run jupyter and open ./is_it_good_mlflow.ipynb 
        
        jupyter notebook

 * run all cells one by one until the pth file is created in `/content/models/`

 * instead of rebuilding the image you can specify the custom model path:

     docker run -p 5080:80 -e API_TOKEN=your_api_token -v /content:/content -e AVATAR_MODEL_PATH=/content/models/resnet_model92.pth avatars-detector

