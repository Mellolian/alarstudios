Для запуска приложения необходимо создать в PostgreSQL базу данный alar командой CREATE DATABASE alar; затем необходимо создать пользователя admin с паролем admin командой CREATE ROLE admin WITH PASSWORD 'admin';
Если порт СУБД отличается от 5433, его значение необходимо присвоить переменной port в файле app.py
Затем необходимо запустить команды:
pip3 install pipenv
pipenv shell
pip3 install -r requirements.txt
flask run
Для удобства в репозитории и письме приложен файл setup.py, который нужно запустить командой pipenv run python3 setup.py, и он в автоматическом режиме скачает проект из репозитория, установит все зависимости и запустит его.
