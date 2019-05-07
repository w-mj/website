from http.cookiejar import CookieJar

import requests
from bs4 import BeautifulSoup
from requests.cookies import RequestsCookieJar

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


def get_table():
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
    page_cookies.set('neu_cas_un', my_neu_id, domain='pass.neu.edu.cn', path='/')

    login_response = requests.post(
        "https://pass.neu.edu.cn/tpass/login?service=http%3A%2F%2F219.216.96.4%2Feams%2FhomeExt.action",
        headers=dict(headers, **{
            'Referer': 'https://pass.neu.edu.cn/tpass/login?service=https%3A%2F%2Fportal.neu.edu.cn%2Ftp_up%2F',
            'Origin': 'https://pass.neu.edu.cn',
            'Host': 'pass.neu.edu.cn',
        }),
        cookies=page_cookies,
        data={
            'rsa': my_neu_id + my_neu_psd + lt,
            'ul': len(my_neu_id),
            'pl': len(my_neu_psd),
            'lt': lt,
            'execution': execution,
            '_eventId': _eventId
        })

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
        'ids': '6869'
    })
    if table_response.content != b'':
        with open('table.html', 'w', encoding='utf-8') as f:
            f.write(table_response.content.decode())


rep = 'activity=newTaskActivity\(.+,.+,"(.+)","(.+)","(.+)","(.+)","(.+)",.+,.+,.+,.+,.+\);\n+index=(' \
      '\d+)\*unitCount\+(\d+);\n+table0\.activities\[index\]\[table0\.activities\[' \
      'index\]\.length\]=activity;\n+index=(\d+)\*unitCount\+(\d+);\n+table0\.activities\[index\]\[' \
      'table0\.activities\[index\]\.length\]=activity;\n+ '

def parse_table(table_str):
    pass


if __name__ == '__main__':
    # get_table()
    with open('table.html', 'r', encoding='utf-8') as f:
        parse_table(f.read())
