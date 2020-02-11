#!/bin/bash

git checkout -- .
git pull origin master
python3 manage.py collectstatic --noinput
ssh root@127.0.0.1 "supervisorctl restart chatbot"
