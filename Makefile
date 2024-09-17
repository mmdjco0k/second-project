run-server :
	python manage.py runserver


migrate :
	python manage.py migrate


migrations :
	python manage.py makemigrations


redis-run :
	sudo docker run -p 6379:6379 --rm -v /tmp/data/redis:/data redis redis-server --appendonly yes
