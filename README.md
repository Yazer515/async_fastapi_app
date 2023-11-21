# Руководство по развёртыванию


## Требования для развёртывания и запуска программы

* ОС == Ubuntu 22.04.1 LTS. Другие ОС не поддерживаются
* Python >= 3.10

## Шаги развёртывания и запуска программы через терминал ubuntu 

1. **Билд контейнера** 
```
sudo docker-compose build
```
2. **Запуск контейнера** 
```
sudo docker-compose up
```
Приложение находится по адресу http://0.0.0.0:8000/docs
