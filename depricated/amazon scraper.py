import asyncio
import time

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

        await asyncio.sleep(20)
        body = await session.get_page_source()      # getting raw HTML.
        parsable_html = HTML(html=body)             # converting to parsable HTML.

        return parsable_html

def get_absolute_links(parsable_html:HTML)->list:
    """Get absolute links from an amazon products list-view."""

    if parsable_html == '':
        return []
        
    relative_links = []     # relative links of product detail.

    div_list = parsable_html.find("div[data-component-type='s-search-result']")  # list of product div

    for div in div_list:
        anchor  = div.find("h2>a")
        href    = anchor[0].attrs['href']
        relative_links.append(href)
    
    absoulute_links = ["https://www.amazon.in"+x for x in relative_links if '/dp/' in x]

    return absoulute_links

async def get_all_absolute_links(product:str, last_page:int):
    """Get absolute links from entire pagination"""
    
    absolute_links = []
    task_list = []
    for i in range(1, last_page+1):
        task_list.append(
            asyncio.create_task(scraper(url.format(product, i)))
        )

    list_of_bodies = await asyncio.gather(*task_list)

    for body in list_of_bodies:
        links = get_absolute_links(body)
        absolute_links.extend(links)
    
    return absolute_links

if __name__ == "__main__":    
    # product = input("insert product")
    product = 'pendrive'
    url = "https://www.amazon.in/s?k={}&page={}"

    start = time.time()     # recording start time.

    body = asyncio.run(scraper(url.format(product, 1)))                     # getting HTML
    last_page = int(body.find("ul.a-pagination > li.a-disabled")[-1].text)  # grabing last page of pagination

    k = asyncio.run(get_all_absolute_links(product, last_page))

    # printing stats
    print(f"Product links gathered: {len(k)}")
    print(f"Time taken: {time.time() - start} sec")

    # saving links to txt file
    with open("links.txt", mode='a') as file_:
        for link in k:
            file_.write(link+'\n')