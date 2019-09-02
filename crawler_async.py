import aiohttp
import asyncio
import uvloop
import json

import pandas as pd


url = "https://api-fact-checker.line-apps.com/pub/v1/zhtw/articles/verified?size=12&sort=updatedAt,desc&page={}"

async def fetch_and_filt(session, page):
    print(page)  #
    async with session.get(url.format(page)) as r:
        # assert (await r.status) == 200

        data = json.loads(await r.text())
        return ([post['id'], post['content'], post['tag']['en'], post['tag']['zhtw']]
                for post in data['content'])

async def fetch_pages(page_range):
    async with aiohttp.ClientSession() as session:
        result = await asyncio.gather(
            *[fetch_and_filt(session, page) for page in page_range]
        )
        return result


pages = 116

async def main():
    global result
    result = await fetch_pages(range(pages))

uvloop.install()
asyncio.run(main())


def flatten(gens):
    for gen in gens:
        yield from gen

source = list(flatten(result))
df = pd.DataFrame(source, columns=['id', 'content', 'tag_en', 'tag_zhtw'])

df.to_csv("line-fact-verified.csv")