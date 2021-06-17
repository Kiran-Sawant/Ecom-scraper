# Ecom-scraper
A web scraper for scraping product information from ecommerce websites. Built using arsenic, requests-html

Launch main.py, It will ask for product name and website. It will scrape the price, title, rating, availability status of all the products that are listed for the query ad return a .csv file with all the data.  
The program uses asyncio to make asynchronous requests with multiple chrome-driver instances. Therefore it requires chrome-driver to extract HTML pages.
Currently it supports amazon.in only
