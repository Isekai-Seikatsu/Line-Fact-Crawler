import requests
import json

import pandas as pd

from itertools import count


url = "https://api-fact-checker.line-apps.com/pub/v1/zhtw/articles/verified?size=12&sort=updatedAt,desc&page={}"

def fetch_and_filt(page):
    print(page)  #
    r = requests.get(url.format(page))
    assert r.ok

    data = json.loads(r.text)
    yield from ([post['id'], post['content'], post['tag']['en'], post['tag']['zhtw']]
                for post in data['content'])

def fetch_pages():
    for page in count():
        contents = list(fetch_and_filt(page))
        if contents:
            yield from contents
        else:
            return


source = list(fetch_pages())

df = pd.DataFrame(source, columns=['id', 'content', 'tag_en', 'tag_zhtw'])

df.to_csv('line-fact-verified.csv')