# Руководство по развёртыванию парсера магазина METRO


## Требования для развёртывания и запуска программы

* ОС == Ubuntu 22.04.1 LTS. Другие ОС не поддерживаются
* Python >= 3.10

## Шаги развёртывания и запуска программы через терминал ubuntu 

1. **Установка библиотек** 
```
pip install -r requirements.txt
```
2. **Запуск приложения** 
```
python main.py
```
## Входные данные
Для запуска парсера необходим файл config.json, который должен находиться в папке config. Для примера оформления файла конфига приведён в пример файл sample_json.json, который содержит следующие поля:
```
category - ссылка на категорию, например, /category/alkogolnaya-produkciya/krepkiy-alkogol/viski
cities - список, который содержит словарь из айди города и самого города
store_id - айди города
city - Название города
```
## Выходные данные
Результат работы представляет собой файл формата .xlsx, в котором содержатся 2 листа с результатом парсинга для 2-х городов
