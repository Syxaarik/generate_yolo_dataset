import os
import shutil
import random
from pathlib import Path
import yaml

# === НАСТРОЙКИ ===
SOURCE_DIR = str(input("Введите название вашей папки dataset: "))
DEST_DIR = 'dataset'
TRAIN_RATIO = 0.8  # 80% - train, 20% - val

# Создаём нужные папки
for split in ['train', 'val']:
    os.makedirs(f'{DEST_DIR}/images/{split}', exist_ok=True)
    os.makedirs(f'{DEST_DIR}/labels/{split}', exist_ok=True)

# Получаем список всех изображений
image_files = list(Path(f'{SOURCE_DIR}/images').glob('*.*'))
random.shuffle(image_files)

split_index = int(len(image_files) * TRAIN_RATIO)
train_files = image_files[:split_index]
val_files = image_files[split_index:]


def move_files(file_list, split):
    for img_path in file_list:
        img_name = img_path.name
        label_name = img_path.with_suffix('.txt').name

        shutil.copy(img_path, f'{DEST_DIR}/images/{split}/{img_name}')
        label_path = Path(f'{SOURCE_DIR}/labels') / label_name
        if label_path.exists():
            shutil.copy(label_path, f'{DEST_DIR}/labels/{split}/{label_name}')


move_files(train_files, 'train')
move_files(val_files, 'val')

# Чтение классов из classes.txt
with open(f'{SOURCE_DIR}/classes.txt', 'r', encoding='utf-8') as f:
    class_names = [line.strip() for line in f.readlines()]

# Создание data.yaml
data_yaml = {
    'train': str(Path(DEST_DIR) / 'images/train'),
    'val': str(Path(DEST_DIR) / 'images/val'),
    'nc': len(class_names),
    'names': class_names
}

with open(f'{DEST_DIR}/data.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(data_yaml, f, allow_unicode=True)

print(f"✅ Датасет готов: {DEST_DIR}/ (train/val + data.yaml)")
