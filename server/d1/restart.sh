# NOTE: This script will kill all django processes.
pkill -f 'python manage.py runserver 0.0.0.0:8000'
export PYTHONIOENCODING=utf-8
python manage.py runserver 0.0.0.0:8000
ps aux | grep --color \[m\]anage\.py
echo "Restart vine succeed!"
