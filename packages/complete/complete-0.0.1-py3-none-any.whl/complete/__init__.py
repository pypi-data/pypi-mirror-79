import requests, aiohttp, json
from urllib.parse import quote
from lxml import etree
class AutoComplete(object):
    def google_complete(query):
        r=requests.get(f"https://www.google.com/complete/search?q={quote(query)}&cp=9&client=psy-ab")
        results=[result[0].replace("<b>","").replace("</b>","") for result in r.json()[1]]
        return results
    def youtube_complete(query):
        r=requests.get(f"https://clients1.google.com/complete/search?client=youtube&q={quote(query)}")
        results=eval(r.text.replace("window.google.ac.h(","").replace(")",""))
        results=[result[0] for result in results[1]]
        return results
    def duckduckgo_complete(query):
        r=requests.get(f"https://duckduckgo.com/ac/?q={quote(query)}")
        results=[x["phrase"] for x in r.json()]
        return results
    def bing_complete(query):
        r=requests.get(f"https://www.bing.com/AS/Suggestions?qry={quote(query)}&cvid=complete")
        root=etree.HTML(r.text)
        contents=root.xpath("//strong/text()")
        return [(query+" " + c) for c in contents]

class AioAutoComplete(object):
    async def google_complete(query):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://www.google.com/complete/search?q={quote(query)}&cp=9&client=psy-ab") as r:
                results=[result[0].replace("<b>","").replace("</b>","") for result in (await r.json())[1]]
                return results
    async def youtube_complete(query):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://clients1.google.com/complete/search?client=youtube&q={quote(query)}") as r:
                results=eval((await r.text()).replace("window.google.ac.h(","").replace(")",""))
                results=[result[0] for result in results[1]]
                return results
    async def duckduckgo_complete(query):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://duckduckgo.com/ac/?q={quote(query)}") as r:
                results=[x["phrase"] for x in (json.loads(await r.read()))]
                return results
    async def bing_complete(query):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://www.bing.com/AS/Suggestions?qry={quote(query)}&cvid=complete") as r:
                root=etree.HTML((await r.text()))
                contents=root.xpath("//strong/text()")
                return [(query+" " + c) for c in contents]
