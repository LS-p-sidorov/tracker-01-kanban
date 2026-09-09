# Tracker 01 — Kanban Django

Минимальный MVP канбан-доски на Django: регистрация, роли (Менеджер/Участник), доски, задачи, перемещение задач (drag-and-drop + селектор статуса).

## Требования

- Python **>= 3.12** (проект создан и проверен на Python 3.14, Django 6.1.1).

Важно: в shell может быть alias `python` на системный интерпретатор (например, Python 3.9).
Поэтому **все команды ниже используют `.venv/bin/python` явно** — не полагайтесь на `python` после `source activate`.

## Локальный запуск (существующее окружение проекта)

```bash
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python manage.py migrate
.venv/bin/python manage.py seed_demo   # опционально: демо-данные
.venv/bin/python manage.py runserver 127.0.0.1:8000
```

Открыть: http://127.0.0.1:8000/

Демо-аккаунты (после `seed_demo`, учебные): `manager / Demo12345!`, `member / Demo12345!`.

Если `.venv` ещё нет, создать (подойдёт любой интерпретатор >= 3.12):

```bash
python3.14 -m venv .venv
```

## Проверка

```bash
.venv/bin/python manage.py check
```

## База данных

Локально — SQLite (`db.sqlite3`). При наличии переменной окружения `DATABASE_URL`
(например, `postgres://...` от Railway) приложение автоматически использует PostgreSQL
(драйвер psycopg v3, настроен через dj-database-url). Примеры — в `.env.example`.

## Деплой на Railway (минимальные действия)

1. Создать сервис из этого репозитория (Nixpacks определит Python и подхватит `Procfile`: `web: gunicorn config.wsgi:application`, `release: migrate + collectstatic`).
2. Подключить к сервису Railway Plugin **PostgreSQL** — переменная `DATABASE_URL` добавится автоматически.
3. Выставить переменные окружения:
   - `DEBUG=0`
   - `SECRET_KEY=<сгенерированный ключ>` (не тот, что в коде)
   - `ALLOWED_HOSTS=<домен railway>` (или `*`)
4. Deploy. Статика раздаётся WhiteNoise из `STATIC_ROOT` (collectstatic выполняется на release-этапе).
