# api_final
api для проекта yatube. API включает позволяет создавать, удалять, получать и изменять записи в моделях. Подробности можно узнать в [документации](https://localhost:8000/redoc).

**Внимание, большинство операций трубуют аутентификацию пользователя.**

### Как запустить проект:

1. Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/ilart/api_final_yatube.git
```

```
cd api_final_yatube
```

2. Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

3. Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

4. Выполнить миграции:

```
python3 manage.py migrate
```

5. Запустить проект:

```
python3 manage.py runserver
```
