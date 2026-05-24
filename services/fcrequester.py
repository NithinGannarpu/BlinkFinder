import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()

DEFAULT_PCODE = os.getenv("FC_DEFAULT_PCODE") 

def fetch_products(page: int = 1, pcode: str = DEFAULT_PCODE):
    url = "https://www.firstcry.com/svcs/SearchResult.svc/GetSearchResultProductsPaging"

    query_string = {
        "PageNo": page,
        "PageSize": "20",
        "SortExpression": "popularity",
        "OnSale": "5",
        "SearchString": "brand",
        "SubCatId": "",
        "BrandId": "",
        "MasterBrand": "113",
        "pcode": pcode,
    }

    

    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "en-US,en;q=0.9",
        "referer": "https://www.firstcry.com/hotwheels/5/0/113?sort=popularity",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest",
        "Cookie": os.getenv("FC_COOKIE"),
    }

    response = requests.get(url, headers=headers, params=query_string)
    response.raise_for_status()  
    return response.json()       

# data = fetch_products(page=1)
# print(data)


def parse_products(response_data: dict) -> list[dict]:
    product_response = json.loads(response_data["ProductResponse"])
    products = product_response["Products"]

    result = []
    for index, product in enumerate(products, start=1):
        result.append({
            "rowIndex": index,
            "PNm": product["PNm"],
            "BNm": product["BNm"],
            "MRP": product["MRP"],
            "Disc": product["Disc"],
            "discprice": product["discprice"],
            "rating": product["rating"],
            "CrntStock": product["CrntStock"],
            "shippingdate": product["shippingdate"],
        })
    return result
