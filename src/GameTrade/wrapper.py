import requests

from bs4 import BeautifulSoup
from ua_parser import user_agent_parser

from assets.random_tools import random_ua, random_string

from recaptcha import anticaptcha_solver

base_url = "https://gametrade.jp/"

def get_cookie():
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Accept': '*/*;q=0.5, text/javascript, application/javascript, application/ecmascript, application/x-ecmascript',
        'Accept-Language': 'ja,en-US;q=0.7,en;q=0.3',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': 'https://gametrade.jp/monst/exhibits',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://gametrade.jp',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Connection': 'keep-alive',
    }
    response = requests.get(base_url + "signin", headers=headers)
    return response.cookies.get_dict()["_session_id"]

def login(email, password):
    ua = random_ua()
    parsed_ua = user_agent_parser.Parse(ua)
    headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://gametrade.jp",
    "Referer": "https://gametrade.jp/signin",
    "Sec-Ch-Ua": '" Not A;Brand";v="99", "Chromium";v="{0}", "Google Chrome";v="{0}"'.format(parsed_ua['user_agent']['major']),
    "Sec-Ch-Ua-Mobile": '?0',
    "Sec-Ch-Ua-Platform": '"{}"'.format(parsed_ua['os']['family']),
    }
    url = base_url + "signin"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, features="lxml")
    found_content = soup.find("meta", attrs={'name': "csrf-token"})
    token = str(found_content).split('"')[1]

    cookie = response.cookies.get_dict()["_session_id"]
    print(cookie)
    cookies = {
        "_session_id": cookie
    }
    data = {
        "utf8": "✓",
        "authenticity_token": token,
        "session[email]": email,
        "session[password]": password,
        "g-recaptcha-response": anticaptcha_solver(url)
    }
    result = requests.post(url, data=data, headers=headers, cookies=cookies)
    print(result.cookies, result, result.text)
    status_code = result.status_code
    if status_code in (200, 201):
        print('[/] Maybe success account login!')
        return False
    elif status_code == 302:
        print("[+] Success Account Creation! ")
        return True
    else:
        print("[-] Maybe Error...")
        return False

def gametrade_token_gen():
    ua = random_ua()
    parsed_ua = user_agent_parser.Parse(ua)
    headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://gametrade.jp",
    "Referer": "https://gametrade.jp/signup_info",
    "Sec-Ch-Ua": '" Not A;Brand";v="99", "Chromium";v="{0}", "Google Chrome";v="{0}"'.format(parsed_ua['user_agent']['major']),
    "Sec-Ch-Ua-Mobile": '?0',
    "Sec-Ch-Ua-Platform": '"{}"'.format(parsed_ua['os']['family']),
    }
    url = base_url + "signup"
    response = requests.get(url, headers=headers).text
    soup = BeautifulSoup(response, features="lxml")
    found_content = soup.find("meta", attrs={'name': "csrf-token"})
    token = str(found_content).split('"')[1]

    nickname = random_string(6)
    email = ""
    password = random_string(10)
    url = base_url + "users"
    data = {
        "utf8": "✓",
        "authenticity_token": token,
        "user[nickname]": nickname,
        "user[email]": email,
        "user[password]": password,
        "invited_user[invite_code]": "",
        "g-recaptcha-response": anticaptcha_solver(url)
    }
    result = requests.post(url, data=data, headers=headers)
    print(result.cookies, email, password)
    status_code = result.status_code
    if status_code in (200, 201):
        print('[/] Maybe success account creation!')
        return False
    elif status_code == 302:
        print("[+] Success Account Creation! ")
        return True
    else:
        print("[-] Maybe Error...")
        return False

def verify_email(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'ja,en-US;q=0.7,en;q=0.3',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Connection': 'keep-alive',
    }

    response = requests.get(url, headers=headers, allow_redirects=True)

def like(url, token, remember_token, session_id):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Accept': '*/*;q=0.5, text/javascript, application/javascript, application/ecmascript, application/x-ecmascript',
        'Accept-Language': 'ja,en-US;q=0.7,en;q=0.3',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': 'https://gametrade.jp/',
        'X-CSRF-Token': token,
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://gametrade.jp',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Connection': 'keep-alive',
    }

    cookies = {
        '_session_id': session_id,
        'remember_token': remember_token,
    }

    data = {
        'utf8': '✓',
        'button': '',
        #"_method": "delete"
    }

    response = requests.post(url, headers=headers, json=data, cookies=cookies)
    print(response.text)
