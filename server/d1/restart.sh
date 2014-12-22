# NOTE: This script will kill all django processes.
# For MAC
pkill -f 'Python manage.py runserver 0.0.0.0:8000'
pkill -f 'Python -m smtpd -n -c DebuggingServer localhost:1025'
# For Linux
pkill -f 'python manage.py runserver 0.0.0.0:8000'
pkill -f 'python -m smtpd -n -c DebuggingServer localhost:1025'

echo "\ncheck utils running...\n"

mongodb=$(ps aux | grep -E "[m]ongo")
if [ -z "$mongodb" ]; then
    echo "mongodb is not running! abort!"
    exit -1
else
    echo "mongodb is running!"
fi

echo "\ncheck utils done...\n"

export PYTHONIOENCODING=utf-8
python -m smtpd -n -c DebuggingServer localhost:1025 &
python manage.py runserver 0.0.0.0:8000
# python manage.py runserver --noreload 0.0.0.0:8000 --nostatic
