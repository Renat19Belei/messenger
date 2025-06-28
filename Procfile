release: python manage.py migrate
web: uvicorn messanger.asgi:app --host 0.0.0.0 --port $PORT