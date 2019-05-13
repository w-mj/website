import datetime

import pytz
import requests
from bs4 import BeautifulSoup
from requests.cookies import RequestsCookieJar
import re

from schedule.ScheduleService.course import Course, Schedule
from website.secrets import my_neu_id, my_neu_psd


User_Agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
headers = {
    'User-Agent': User_Agent,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
}


class NEUSchedule(Schedule):
    def __init__(self):
        super().__init__()
        self.first_week = datetime.datetime(year=2019, month=3, day=3, tzinfo=pytz.timezone("Asia/Shanghai"))
        self.name = None

    def update(self, **kwargs):
        login_page_url = "https://pass.neu.edu.cn/tpass/login?service=http%3A%2F%2F219.216.96.4%2Feams%2FhomeExt.action"

        login_page_response = requests.get(login_page_url, headers={'User-Agent': User_Agent})
        if login_page_response.status_code != 200:
            print("Get login page error")

        login_page = BeautifulSoup(login_page_response.content.decode(), features='html.parser')
        page_cookies = login_page_response.cookies
        # login_page = BeautifulSoup(open("test_html.txt", encoding='utf-8').read())

        # rsa = login_page.find(id="rsa")['value']
        # ul = login_page.find(id="ul")['value']
        # pl = login_page.find(id="pl")['value']
        login_form = login_page.find(id="loginForm")
        login_url = login_form['action']
        lt = login_page.find(id="lt")['value']
        execution = login_form.find("input", attrs={'name': 'execution'})['value']
        _eventId = login_form.find("input", attrs={'name': '_eventId'})['value']
        # rsa=20164617310410LT-3067-QjgEomOwuvnc0lIxzRWXafjreJ1i6u-tpass&
        # ul=8&
        # pl=6&
        # lt=LT-3067-QjgEomOwuvnc0lIxzRWXafjreJ1i6u-tpass&
        # execution=e2s1&
        # _eventId=submit

        # page_cookies['neu_cas_un'] = my_neu_id
        page_cookies.set('neu_cas_un', kwargs['uid'], domain='pass.neu.edu.cn', path='/')

        login_response = requests.post(
            "https://pass.neu.edu.cn/tpass/login?service=http%3A%2F%2F219.216.96.4%2Feams%2FhomeExt.action",
            headers=dict(headers, **{
                'Referer': 'https://pass.neu.edu.cn/tpass/login?service=https%3A%2F%2Fportal.neu.edu.cn%2Ftp_up%2F',
                'Origin': 'https://pass.neu.edu.cn',
                'Host': 'pass.neu.edu.cn',
            }),
            cookies=page_cookies,
            data={
                'rsa': kwargs['uid'] + kwargs['password'] + lt,
                'ul': len(kwargs['uid']),
                'pl': len(kwargs['password']),
                'lt': lt,
                'execution': execution,
                '_eventId': _eventId
            })

        login_response_page = BeautifulSoup(login_response.content.decode(), features='html.parser')
        stu_name = login_response_page.find('a', {'class': 'personal-name'})
        if stu_name is None:
            return False
        stu_name = stu_name.text.strip()
        self.name = stu_name.split('(')[0]
        print(stu_name)

        if login_response.content != b'':
            with open('login_response.html', 'w', encoding='utf-8') as f:
                f.write(login_response.content.decode('utf-8'))
        if '教学周' in login_response.content.decode('utf-8'):
            print("登录成功")

        cookies_209 = RequestsCookieJar()

        histories = [login_page_response] + login_response.history + [login_response]
        for h in histories:
            for c in h.cookies:
                c.domain = h.url.split('/')[2]
                print(c)
                cookies_209.set_cookie(c)

        ids_url = 'http://219.216.96.4/eams/courseTableForStd.action?_=1557724872728'
        ids_response = requests.get(ids_url, cookies=cookies_209)
        ids = re.findall('bg\.form\.addInput\(form,"ids","(.+)"\);', ids_response.content.decode())

        table_url = 'http://219.216.96.4/eams/courseTableForStd!courseTable.action'
        # semester.id=30: 2018-2019春季学期
        table_response = requests.post(table_url, cookies=cookies_209, headers=dict(headers, **{
            'Host': '219.216.96.4',
            'Origin': 'http://219.216.96.4',
            'Referer': 'http://219.216.96.4/eams/courseTableForStd.action'
        }), data={
            'ignoreHead': '1',
            'showPrintAndExport': '1',
            'setting.kind': 'std',
            'startWeek': '',
            'semester.id': '30',
            'ids': ids[0]
        })
        if table_response.content != b'':
            with open('table.html', 'w', encoding='utf-8') as f:
                f.write(table_response.content.decode())
        table_str = table_response.content.decode()
        table_str = table_str.replace(' ', '')
        table_str = table_str.replace('\t', '')
        # table_str = table_str.replace('\r', '').replace('\n', '')
        with open('table2.html', 'w', encoding='utf-8') as f:
            f.write(table_str)
        with open('table2.html', encoding='utf-8') as f:
            stt = f.read()
            print(stt == table_str)
            self.parse_table(stt)
        return True

    rep = 'activity=newTaskActivity\(.+,.+,"(.+)","(.+)","(.+)","(.+)","(.+)",.+,.+,.+,.+,.+\);\n*' \
          'index=(\d+)\*unitCount\+(\d+);\n*'\
          'table0\.activities\[index\]\[table0\.activities\[index\]\.length\]=activity;\n*'\
          'index=(\d+)\*unitCount\+(\d+);\n*'\
          'table0\.activities\[index\]\[table0\.activities\[index\]\.length\]=activity;'
    repc = re.compile(rep)
    start_time_table = [
        datetime.timedelta(hours=8, minutes=30),
        datetime.timedelta(hours=9, minutes=30),
        datetime.timedelta(hours=10, minutes=40),
        datetime.timedelta(hours=11, minutes=40),
        datetime.timedelta(hours=14, minutes=00),
        datetime.timedelta(hours=15, minutes=00),
        datetime.timedelta(hours=16, minutes=10),
        datetime.timedelta(hours=17, minutes=10),
        datetime.timedelta(hours=18, minutes=30),
        datetime.timedelta(hours=19, minutes=30),
        datetime.timedelta(hours=20, minutes=40),
        datetime.timedelta(hours=21, minutes=40),
    ]
    end_time_table = [
        datetime.timedelta(hours=9, minutes=20),
        datetime.timedelta(hours=10, minutes=20),
        datetime.timedelta(hours=11, minutes=30),
        datetime.timedelta(hours=12, minutes=30),
        datetime.timedelta(hours=14, minutes=50),
        datetime.timedelta(hours=15, minutes=50),
        datetime.timedelta(hours=17, minutes=00),
        datetime.timedelta(hours=18, minutes=00),
        datetime.timedelta(hours=19, minutes=20),
        datetime.timedelta(hours=20, minutes=20),
        datetime.timedelta(hours=21, minutes=30),
        datetime.timedelta(hours=22, minutes=30),
    ]

    def parse_table(self, table_str):
        searched = self.repc.findall(table_str)

        for course in searched:
            print('编号：{}，课名：{}，地点{}，星期：{}，{}-{}节，上课周：{}'.format(
                course[0], course[1], course[3], (int(course[5]) + 1) % 7, int(course[6]) + 1, int(course[8]) + 1, course[4]
            ))
            # course[4] += '0'
            start_week = 0
            for i in range(len(course[4])):
                if course[4][i] == '0' and (i == len(course[4]) - 1 or course[4][i + 1] == '1'):
                    start_week = i + 1
                elif course[4][i] == '1' and (i == len(course[4]) - 1 or course[4][i + 1] == '0'):
                    c = Course()
                    c.id = course[0]
                    c.name = course[1]
                    c.location = course[3]
                    c.day = (int(course[5]) + 1) % 7
                    c.sweek = start_week
                    c.eweek = i
                    c.stime = self.start_time_table[int(course[6])]
                    c.etime = self.end_time_table[int(course[8])]
                    self.course_list.append(c)


if __name__ == '__main__':
    # get_table()
    s = NEUSchedule()
    s.update(uid=my_neu_id, password=my_neu_psd)
    # with open('table2.html', 'r', encoding='utf-8') as f:
    #     stt = f.read()
    #     s.parse_table(stt)
    calendar = s.get_calendar()
    ics_str = calendar.to_ical().decode()
    print(ics_str)
    with open('a.ics', 'w', encoding='utf-8') as f:
        f.write(ics_str)

