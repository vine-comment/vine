# NOTE: This script will kill all django processes.
sudo pkill -f 'python manage.py runserver 0.0.0.0:8000'
sudo pkill -f 'python -m smtpd -n -c DebuggingServer localhost:1025'
export PYTHONIOENCODING=utf-8
python -m smtpd -n -c DebuggingServer localhost:1025 &
python manage.py runserver 0.0.0.0:8000
# python manage.py runserver --noreload 0.0.0.0:8000 --nostatic
