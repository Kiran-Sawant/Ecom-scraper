import asyncio
from typing import List

from requests_html import HTML

from .scraper import scraper

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

async def get_all_absolute_links(product:str):
    """Get absolute links from entire pagination"""

    url = "https://www.amazon.in/s?k={}&page={}"

    # body = await scraper(url.format(product, 1))                     # getting HTML
    # last_page = int(body.find("ul.a-pagination > li.a-disabled")[-1].text)  # grabing last page of pagination
    
    absolute_links = []
    task_list = []
    
    # for i in range(1, last_page + 1):
    for i in range(1, 2):
        task_list.append(
            asyncio.create_task(scraper(url.format(product, i)))
        )

    list_of_bodies = await asyncio.gather(*task_list)

    for body in list_of_bodies:
        links = get_absolute_links(body)
        absolute_links.extend(links)
    
    return absolute_links

#___________Product Detail______________#
def get_product_price(html:HTML):

    price_elm = html.find("span[id^=priceblock_]")[0]
    price_raw = price_elm.text

    currency, price = tuple(price_raw.replace('\xa0', ' ').split(' '))
    price = float(price)

    return (currency, price)

def get_availability(html:HTML)->bool:
    stock_elm = html.find("div#availability")[0]
    available = stock_elm.text

    if available == 'In stock.':
        return True
    else:
        return False

def get_title(html:HTML)->str:

    title_elm = html.find("span#productTitle")[0]
    title = title_elm.text

    return title

def get_rating(html:HTML)->str:

    ratings = html.find("span.a-icon-alt")
    rating_elm = ratings[0]

    return float(rating_elm.text.split(' ')[0])

async def get_product_detail(urls:List[str])->List[dict]:

    # url = "https://www.amazon.in/AmazonBasics-AZHDAD01-HDMI-Coupler-Black/dp/B06XR9PR5X/"

    list_of_detail = []
    task_list = []

    for link in urls[0:5]:
        task_list.append(
            asyncio.create_task(scraper(link))
        )
    
    product_pages = await asyncio.gather(*task_list)
        
    for product_page in product_pages:

        detail = dict()

        available = get_availability(product_page)
        if available:
            price_data = get_product_price(product_page)

            detail["available"]    = available
            detail["currency"]     = price_data[0]
            detail["price"]        = price_data[1]
            detail["title"]        = get_title(product_page)
            detail["rating"]       = get_rating(product_page)
        
        else:
            detail["available"]    = 'not available'
            detail["price"]        = None
            detail["title"]        = get_title(product_page)
            detail["rating"]       = None

        list_of_detail.append(detail)

    return list_of_detail
    # print(task_list)
    # return product_pages

async def run_amazon(product:str):

        product_links = await get_all_absolute_links(product)

        product_details = await get_product_detail(product_links)

        return product_details



        