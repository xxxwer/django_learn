#########################################################################
# File Name: runserver.sh
# Author: ma6174
# mail: ma6174@163.com
# Created Time: 2017年09月08日 星期五 15时49分35秒
#########################################################################
#!/bin/bash
# python manage.py runserver 0.0.0.0:9999
# socket = /home/wer/realwork/djangoLearn/freeLink/freelink.sock
sudo /home/wer/.virtualenvs/py3scrapy/bin/uwsgi --ini /home/wer/realwork/djangoLearn/freeLink/uwsgi.ini > /var/log/www_freelink.log 2>&1

