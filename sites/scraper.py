import asyncio
from arsenic import (services, browsers, get_session)
from requests_html import HTML

async def scraper(url:str)->HTML:

    # setting-up arsenic
    service = services.Chromedriver()
    browser = browsers.Chrome()
    browser.capabilities = {
        'goog:chromeOptions': {'args': ['--headless', '--disable-gpu']}
    }

    # creating a session
    async with get_session(service, browser) as session:
        try:
            await asyncio.wait_for(session.get(url), timeout=120)   # opening URL
        except asyncio.TimeoutError:
            return ''

        # await asyncio.sleep(20)
        body = await session.get_page_source()      # getting raw HTML.
        parsable_html = HTML(html=body)             # converting to parsable HTML.

        return parsable_html