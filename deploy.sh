#!/bin/bash

git pull origin master
uwsgi --reload uwsgi.pid
