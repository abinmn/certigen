release: python certigen/manage.py migrate --noinput
web: gunicorn --pythonpath certigen certigen.wsgi