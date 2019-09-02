import requests
import json

import pandas as pd


url = "https://api-fact-checker.line-apps.com/pub/v1/zhtw/articles/verified?size=12&sort=updatedAt,desc&page={}"

def fetch_and_filt(page):
    print(page)  #
    r = requests.get(url.format(page))
    assert r.ok

    data = json.loads(r.text)
    yield from ([post['id'], post['content'], post['tag']['en'], post['tag']['zhtw']]
                for post in data['content'])

def fetch_pages(page_range):
    for page in page_range:
        yield from fetch_and_filt(page)


pages = 116
gen = fetch_pages(range(pages))

source = list(gen)

df = pd.DataFrame(source, columns=['id', 'content', 'tag_en', 'tag_zhtw'])

df.to_csv('line-fact-verified.csv')