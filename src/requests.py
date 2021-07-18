import requests
import time


def getPage(url):
    print('calling api: ' + url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36',
        'Accept': '*/*',
        'Content-Type': 'text/html; charset=utf-8',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'
    }
    page = requests.request("GET", url, headers=headers, data={})
    print(page.status_code)
    if (page.status_code == 200):
        return page.text
    elif (page.status_code == 403):
        print('retrying in 5 secs')
        time.sleep(5)
        return getPage(url)
    return ''
