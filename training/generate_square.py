import os
import numpy as np
from PIL import Image


# Путь к папке для сохранения изображений
output_folder = '/content/avatars/bad'

os.makedirs(output_folder, exist_ok=True)

# Генерация 10 изображений
for i in range(25):
    # Генерация одного случайного цвета RGB
    random_color = np.random.randint(0, 256, size=(3,), dtype=np.uint8)
    
    # Создание массива, заполненного этим цветом
    color_image = np.zeros((100, 100, 3), dtype=np.uint8)
    color_image[:] = random_color
    
    # Получение шестнадцатеричного кода цвета
    hex_color = ''.join([f'{c:02X}' for c in random_color])
    
    # Создание изображения из массива
    img = Image.fromarray(color_image, 'RGB')
    
    # Имя файла в формате "square_FFFFFF.png"
    file_name = f'square_{hex_color}.png'
    
    # Сохранение изображения
    img.save(os.path.join(output_folder, file_name))

print(f"25 изображений сохранены в папке '{output_folder}'")
