web: gunicorn waste_management.wsgi --log-file -
release: python manage.py migrate && python manage.py collectstatic --noinput && python setup_demo.py