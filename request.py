import urllib
import requests
import bs4 as BeautifulSoup
import time
import os
import shutil

HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko)'
                         ' Chrome/23.0.1271.64 Safari/537.11'}
RETRY_COUNT = 5


def request_with_retry(url, retry=RETRY_COUNT, soup=True, headers=HEADERS):
    ok = 0
    while ok < retry:
        try:
            req = urllib.request.Request(url, headers=headers)
            res = urllib.request.urlopen(req)
            if soup:
                res = BeautifulSoup.BeautifulSoup(res, "lxml")
            return res
        except Exception as e:
            print(f'Error: {url} because of "{e}"')
            time.sleep(10)
            ok += 1


def request_stream(url, payload={}, headers=HEADERS, retry=RETRY_COUNT):
    ok = 0
    while ok < retry:
        r = requests.get(url, stream=True, data=payload, headers=headers)
        if r.status_code == 200:
            return r.raw
        elif r.status_code == 429:  # spam
            time.sleep(1)
        else:
            print(r.status_code, url)
        ok += 1


def download_file(url, headers=HEADERS):
    if len(url) == 2:
        filename, url = url
    else:
        filename = url_to_filename(url)

    if os.path.exists(filename):
        return filename
    raw = request_stream(url, headers=headers)
    with open(filename, 'wb') as file:
        shutil.copyfileobj(raw, file)
    return filename


def url_to_filename(url):
    filename = url.split(':')[1]

    while '/' in filename:
        filename = filename.replace('/', ' ')
    return filename


def filename_to_url(filename):
    url = filename
    while ' ' in url:
        url = url.replace(' ', '/')
    return 'https:' + url
