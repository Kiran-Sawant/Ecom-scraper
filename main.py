import asyncio
import time

from sites.amazon import run_amazon
from sites.amazon import get_product_detail as ama_pdetail
from sites.flipkart import get_all_absolute_links as f_get
from storage import (list_to_df, df_to_csv)

def exp(num:int):
    return num + 10

site_dict = {
    'a': run_amazon,
    'f': f_get,
    'e': exp
}


if __name__ == "__main__":    
    product = input("insert product: ")
    site    = input("insert site: ")
    # product = 'pendrive'

    start = time.time()     # recording start time.

    product_details = asyncio.run(site_dict[site](product))

    product_detail_df = list_to_df(product_details)
    df_to_csv(product_detail_df, "my_file.csv")

    # printing stats
    # print(f"Product links gathered: {len(product_links)}")
    print(f"Time taken: {time.time() - start} sec")

    # saving links to txt file
    # with open("links.txt", mode='w') as file_:
    #     for link in product_links:
    #         file_.write(link+'\n')
