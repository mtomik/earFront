#!/bin/sh

# wait for RabbitMQ server to start
sleep 10

# run Celery worker for our project myproject with Celery configuration stored in Celeryconf
celery worker -A earDetectionWebApp -Q default -n default@%h
#celery worker -A earDetectionWebApp -Q default --concurrency=10 -n default@%h
#nohup flower -A earDetectionWebApp.celery  --port=5555 &

#parallel -j 2 -- 'celery worker -A earDetectionWebApp -Q default -n default@%h' 'flower -A earDetectionWebApp.celery --port=5555'

# funguje spolu s flower ( ale nie logy )
#supervisord -n -c /etc/supervisor/supervisord.conf