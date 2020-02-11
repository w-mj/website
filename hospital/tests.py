import json
import os
from unittest import TestCase

import django
from django.test import Client

from .models import *
import requests
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")
django.setup()
url = 'http://127.0.0.1/hospital/'
headers = {'Content-Type': 'application/json'}

class Test(TestCase):
    def setUp(self):
        u = User()
        u.openid = 123
        u.save()

    def test_uploadill(self):
        client = Client()
        req = client.post(url + 'ill', data={
            'pid': "患者编号xx001",
            'name': "张三",
            'age': 42,
            'gender': 1,
            'ill': "高血压",
            'wechat': "123",
            'info': "患者状态",
            'location': "沈阳市火石桥村1号",
            'pics': [101, 12, 23]
        }, content_type='application/json')
        self.assertEqual(req.content, b'123')
