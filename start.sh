#!/bin/bash
gunicorn her_beauty_hub.wsgi:application --bind 0.0.0.0:${PORT:-8000}

