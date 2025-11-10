web: gunicorn her_beauty_hub.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --threads 2 --timeout 60 --max-requests 1000 --max-requests-jitter 50 --log-file - --access-logfile - --error-logfile -
