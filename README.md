Данный скрипт на Python позволяет перевести обычный dataset в yolo формат
всё что нужно для этого - это обычный dataset с такой структурой:

# dataset/
## ├── images/
### │   ├── image1.jpg
### │   ├── image2.jpg
## ├── labels/
### │   ├── image1.txt
### │   ├── image2.txt
## ├── classes.txt (список всех классов: car, cat, home ...)

затем нужен данный dataset поместить в туже директорию что и сам скрипт и просто запустить его. Но прежде нужно загрузить библиотеку PyYAML --> pip install PyYAML

