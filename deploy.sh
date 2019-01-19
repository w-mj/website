#!/bin/bash

git checkout -- .
git pull origin master
python3 manage.py collectstatic
uwsgi --reload uwsgi.pid
