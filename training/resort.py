#!/usr/bin/env python
# coding: utf-8

import torch
import torch.nn as nn
import torchvision.transforms as transforms
from torchvision import models
from PIL import Image
import os
import shutil
import pathlib


file_path = pathlib.Path(__file__).parent.absolute()

# Путь к файлу модели
model_path = f'{file_path}/../app/models/resnet_model91.81.pth'

# Путь к исходным папкам с изображениями
source_folder = '/content/avatars'
bad_folder = os.path.join(source_folder, 'bad')
good_folder = os.path.join(source_folder, 'good')

# Путь к новым папкам для копирования изображений
new_folder = '/content/avatars_new.9181'
new_bad_folder = os.path.join(new_folder, 'bad')
new_good_folder = os.path.join(new_folder, 'good')
new_unsure_folder = os.path.join(new_folder, 'unsure')
os.makedirs(new_bad_folder, exist_ok=True)
os.makedirs(new_good_folder, exist_ok=True)
os.makedirs(new_unsure_folder, exist_ok=True)

# Функция для загрузки модели
def load_model(model_path):
    model = models.resnet18(pretrained=False)
    num_features = model.fc.in_features
    model.fc = nn.Linear(num_features, 2)  # 2 класса
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
    model.eval()  # Переключение модели в режим оценки
    return model

# Функция для оценки изображения
def predict(model, image_path, transform):
    image = Image.open(image_path)
    if image.mode != 'RGB':
        image = image.convert('RGB')
    image = transform(image).unsqueeze(0)
    with torch.no_grad():
        outputs = model(image)
        probabilities = torch.nn.functional.softmax(outputs, dim=1)
        _, predicted = torch.max(outputs, 1)
        #print(outputs)
        #print(probabilities)
        #print(predicted)

    return predicted.item(), probabilities.squeeze().tolist()

# Функция для оценки изображений и копирования в новые папки
def evaluate_and_copy(model, source_folder, new_bad_folder, new_good_folder):
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    for category in ['bad', 'good']:
        folder = os.path.join(source_folder, category)
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            if os.path.isfile(file_path):
                predicted, probabilities = predict(model, file_path, transform)
                target_folder = new_good_folder 
                if probabilities[0] > 0.8:
                    target_folder = new_bad_folder 
                elif probabilities[1] > 0.8:
                    target_folder = new_good_folder 
                else:
                    target_folder = new_unsure_folder 
                shutil.copy(file_path, os.path.join(target_folder, filename))
                print(f"File {filename} copied to {target_folder} with probabilities {probabilities[0]:.3f} {probabilities[1]:.3f}")

# Загрузка модели
model = load_model(model_path)

# Оценка и копирование изображений
evaluate_and_copy(model, source_folder, new_bad_folder, new_good_folder)
