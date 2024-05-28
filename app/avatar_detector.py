import torch
from torchvision import models
import torch.nn as nn
import torchvision.transforms as transforms

DEVICE = 'cpu' # 'cuda' if torch.cuda.is_available() else 'cpu'
RESNET_MODEL_PATH = 'models/resnet_model91.81.pth'

def load_model(model_path=RESNET_MODEL_PATH):
    model = models.resnet18(weights=None) # pretrained=False
    num_features = model.fc.in_features
    model.fc = nn.Linear(num_features, 2)  # Binary classification
    model.load_state_dict(torch.load(model_path, map_location=DEVICE))
    model = model.to(DEVICE)
    model.eval()
    return model

def classify(resnet_model, image):
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    image = transform(image).unsqueeze(0).to(DEVICE)
    with torch.no_grad():
        output = resnet_model(image)
        probabilities = torch.nn.functional.softmax(output, dim=1).tolist()
        _, predicted = torch.max(output.data, 1)
    # return 'AVATAR_OK' if predicted.item() == 1 else 'AVATAR_INVALID'
    return {"good": probabilities[0][1], "bad": probabilities[0][0]}
