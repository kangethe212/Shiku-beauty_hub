#!/usr/bin/env python
import os
import subprocess
import sys

port = os.environ.get('PORT', '8000')
cmd = [
    'gunicorn',
    'her_beauty_hub.wsgi:application',
    '--bind', f'0.0.0.0:{port}',
    '--workers', '2',
    '--threads', '2',
    '--timeout', '60'
]

sys.exit(subprocess.call(cmd))

