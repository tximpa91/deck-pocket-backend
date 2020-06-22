web: daphne deck_pocket_backend.asgi:application --port $PORT --bind 0.0.0.0
worker: python manage.py runworker channels --settings=deck_pocket_backend.settings -v2