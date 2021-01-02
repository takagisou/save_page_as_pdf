import asyncio
from pyppeteer import launch
from urllib.parse import urlparse
import os

async def main(url: str):
    path = get_url_without_scheme(url)
    dir = mkdir_if_not_exists(path)
    browser = await launch()
    page = await browser.newPage()
    # opts = {"waitUntil": "networkidle", "networkIdleTimeout": 5000}
    await page.goto(url)
    config = {
        "path": "{}/page.pdf".format(dir),
        "format": "A4",
        "printBackground": True
        }
    await page.emulateMedia('screen')
    pdf = await page.pdf(config)
    await browser.close()

def get_url_without_scheme(url: str) -> str:
    parsed = urlparse(url)
    scheme = "{}://".format(parsed.scheme)
    return parsed.geturl().replace(scheme, '')

def get_last_path(url: str) -> str:
    return url.rsplit('/', 1)[-1]

def mkdir_if_not_exists(path: str) -> str:
    dir = "./pdfs/{}".format(path)
    os.makedirs(dir, exist_ok=True)
    return dir

url = "https://github.com/takagisou/save_page_as_pdf"
asyncio.get_event_loop().run_until_complete(main(url))
