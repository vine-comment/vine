# NOTE: This script will kill all django processes.
pkill -i -f 'python manage.py runserver 0.0.0.0:8000'
pkill -i -f 'python -m smtpd -n -c DebuggingServer localhost:1025'
export PYTHONIOENCODING=utf-8
python -m smtpd -n -c DebuggingServer localhost:1025 &
python manage.py runserver 0.0.0.0:8000
