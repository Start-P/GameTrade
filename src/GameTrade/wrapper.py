import requests

from bs4 import BeautifulSoup
from ua_parser import user_agent_parser

from assets.random_tools import random_ua, random_string


base_url = "https://gametrade.jp/"
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
    email = "email"
    password = random_string(10)
    url = base_url + "users"
    data = {
        "utf8": "✓",
        "authenticity_token": token,
        "user[nickname]": nickname,
        "user[email]": email,
        "user[password]": password,
        "invited_user[invite_code]": "",
        #"g-recaptcha-response": g_recaptcha_response
    }
    result = requests.post(url, data=data, headers=headers)
    status_code = result.status_code
    if status_code in (200, 201):
        print('[-] Failed Account Creation with captcha error')
        return False
    elif status_code == 302:
        print("[+] Success Account Creation! ")
        return True
    else:
        print("[-] Maybe Error...")
        return False

gametrade_token_gen()
