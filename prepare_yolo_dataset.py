import os
import shutil
import random
from pathlib import Path
import yaml

# === НАСТРОЙКИ ===
SOURCE_DIR = input("Введите название вашей папки dataset (например, yolo_dataset): ").strip()
DEST_DIR = 'dataset'
TRAIN_RATIO = 0.8  # 80% - train, 20% - val

# Проверка наличия необходимых папок
assert Path(SOURCE_DIR).exists(), f"❌ Папка '{SOURCE_DIR}' не найдена"
assert (Path(SOURCE_DIR) / 'images').exists(), "❌ В папке нет подпапки 'images'"
assert (Path(SOURCE_DIR) / 'labels').exists(), "❌ В папке нет подпапки 'labels'"
assert (Path(SOURCE_DIR) / 'classes.txt').exists(), "❌ Не найден файл 'classes.txt'"

# Создаём нужные папки
for split in ['train', 'val']:
    os.makedirs(f'{DEST_DIR}/images/{split}', exist_ok=True)
    os.makedirs(f'{DEST_DIR}/labels/{split}', exist_ok=True)

# Поддерживаемые форматы изображений
image_extensions = ('.jpg', '.jpeg', '.png')

# Получаем и перемешиваем изображения
image_files = [p for p in Path(f'{SOURCE_DIR}/images').glob('*') if p.suffix.lower() in image_extensions]
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
        else:
            print(f"⚠️ Метка не найдена для {img_name}, пропускается.")


move_files(train_files, 'train')
move_files(val_files, 'val')

# Чтение классов
with open(f'{SOURCE_DIR}/classes.txt', 'r', encoding='utf-8') as f:
    class_names = [line.strip() for line in f if line.strip()]

# Создание корректного data.yaml
data_yaml = {
    'train': f'{DEST_DIR}/images/train',
    'val': f'{DEST_DIR}/images/val',
    'nc': len(class_names),
    'names': class_names
}

with open(f'{DEST_DIR}/data.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(data_yaml, f, allow_unicode=True, sort_keys=False)

print("\n✅ Датасет успешно подготовлен!")
print(f"➡️ Обучение: {data_yaml['train']}")
print(f"➡️ Валидация: {data_yaml['val']}")
print(f"➡️ YAML: {DEST_DIR}/data.yaml")
print(f"➡️ Классов: {len(class_names)}")
