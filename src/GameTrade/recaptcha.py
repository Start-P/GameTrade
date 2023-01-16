import requests
import time

api = "key"

def anticaptcha_solver(url):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }

    json_data = {
        'clientKey': api,
        'task': {
            'type': 'RecaptchaV2TaskProxyless',
            'websiteURL': url,
            'websiteKey': '6Le806QeAAAAAPAPS1HufPdR-c4wvdJcgqif7cFO',
            'minScore': 0.7,
        },
        'softId': 0,
    }

    response = requests.post('https://api.anti-captcha.com/createTask', headers=headers, json=json_data)
    print(response.json())
    task_id = response.json()["taskId"] 

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }

    json_data = {
        'clientKey': api,
        'taskId': task_id,
    }

    response = requests.post('https://api.anti-captcha.com/getTaskResult', headers=headers, json=json_data).json()
    print(response)
    while response["status"] != "ready":
        response = requests.post('https://api.anti-captcha.com/getTaskResult', headers=headers, json=json_data).json()
        print(response)
        time.sleep(3)
    print(response)
    return response["solution"]["gRecaptchaResponse"]
