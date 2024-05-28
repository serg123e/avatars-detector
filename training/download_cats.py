import os
import re
import argparse
import requests
from PIL import Image
from io import BytesIO
from duckduckgo_search import DDGS

def sanitize_filename(filename):
    return re.sub(r'[^a-zA-Z0-9]', '_', filename)

def download_images(query, num_images, output_folder):
    # Создание папки для сохранения изображений, если она не существует
    os.makedirs(output_folder, exist_ok=True)
    
    # Инициализация объекта поиска
    ddgs = DDGS()
    
    # Поиск изображений
    results = ddgs.images(query, max_results=num_images)
    
    for i, result in enumerate(results):
        try:
            # Получение URL изображения
            img_url = result['image']
            response = requests.get(img_url)
            response.raise_for_status()  # Проверка на ошибки
            
            # Загрузка изображения
            img = Image.open(BytesIO(response.content))
            
            # Сохранение изображения
            sanitized_query = sanitize_filename(query)
            img_path = os.path.join(output_folder, f'{sanitized_query}_{i+1}.png')
            img.save(img_path)
            print(f'Изображение сохранено: {img_path}')
        
        except Exception as e:
            print(f'Не удалось загрузить изображение {i+1}: {e}')

if __name__ == '__main__':
    # Настройка аргументов командной строки
    parser = argparse.ArgumentParser(description='Скачивание изображений по запросу с помощью DuckDuckGo')
    parser.add_argument('query', type=str, help='Запрос для поиска изображений')
    parser.add_argument('--num_images', type=int, default=10, help='Количество изображений для загрузки')
    parser.add_argument('--output_folder', type=str, default='downloaded_images', help='Папка для сохранения изображений')
    
    args = parser.parse_args()
    
    # Вызов функции для скачивания изображений
    download_images(args.query, args.num_images, args.output_folder)
