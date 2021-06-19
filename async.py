import asyncio, aiohttp
import json
import requests
from flask import Flask, request, jsonify, render_template, send_from_directory

from pprint import pprint

URL = 'http://127.0.0.1:5000/api'

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()

async def main():
    tasks = []
    async with aiohttp.ClientSession() as session:
        tasks.append(fetch(session, URL))
        htmls = await asyncio.gather(*tasks)
    data = []
    for lst in htmls:
        data.extend(lst)
    
    data = (sorted(data, key=lambda x: x.get('id')))
    # pprint(data)
    return data

def result():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    data = asyncio.run(main())
    print(data)



if __name__ == '__main__':
    result()
