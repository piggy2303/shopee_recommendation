import os
import json
import requests


def requests_get(endpoint: str, params: dict) -> dict:
    base_url = 'https://shopee.vn/api/v4/' + endpoint
    r = requests.get(base_url, params=params)
    r = r.json()
    return r


def save_to_file(data, file_name):
    with open(file_name, 'w') as f:
        json.dump(data, f)
        print("saving done", file_name)


def file_exists(file_name):
    if os.path.exists(file_name):
        return True
    return False


def craw_shop_list():
    if not file_exists('./data/list_shop.json'):
        params = {
            "need_zhuyin": 0,
            "category_id": 11036132
        }
        r = requests_get('official_shop/get_shops_by_category', params)
        save_to_file(r, './data/list_shop.json')
    print("crawl_shop_list done")


def craw_item_from_shop(shop_id: int) -> None:
    params = {
        "by": "pop",
        "entry_point": "ShopByPDP",
        "limit": 100,
        "match_id": shop_id,
        "newest": 0,
        "order": "desc",
        "page_type": "shop",
        "scenario": "PAGE_OTHERS",
        "version": 2
    }

    file_name = './data/raw_data/' + str(shop_id) + '.json'
    if not file_exists(file_name):
        r = requests_get('search/search_items', params)
        save_to_file(r, file_name)


def craw_item_list():
    list_shop = json.load(open('./data/list_shop.json'))
    list_shop = list_shop["data"]["brands"]

    # print(list_shop)
    for list_shop_1 in list_shop:
        # print(list_shop_1["index"])
        for list_shop_2 in list_shop_1["brand_ids"]:
            # print(list_shop_2["shopid"])
            craw_item_from_shop(list_shop_2["shopid"])
    print("craw_item_list done")


def craw_item_details():
    list_file_json = os.listdir("./data/raw_data")

    for file_json in list_file_json:

        file = open("./data/raw_data/" + file_json, 'r')
        data = json.load(file)["items"]

        for i in data:
            i = i["item_basic"]
            itemid = i["itemid"]
            shopid = i["shopid"]

            params = {"itemid": itemid, "shopid": shopid}

            file_name = './data/item_data/' + \
                str(shopid) + "_" + str(itemid) + '.json'
            if not file_exists(file_name):
                r = requests_get('item/get', params)
                r = r["data"]
                save_to_file(r, file_name)
    print("craw_item_details done")


def craw_shop_details():
    list_file_json = os.listdir("./data/raw_data")

    for shopid in list_file_json:
        shopid = shopid.split('.')[0]
        params = {"shopid": shopid}

        file_name = './data/shop_data/' + str(shopid) + '.json'

        if not file_exists(file_name):
            r = requests_get('product/get_shop_info', params)
            r = r["data"]
            save_to_file(r, file_name)
    print("craw_shop_details done")


def create_nest_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)


if __name__ == "__main__":
    # get list of shop
    # save to file ./data/list_shop.json
    craw_shop_list()

    create_nest_folder("./data/raw_data")
    # get list of items from shop
    # save list of result to file ./raw_data/[shop_id].json
    craw_item_list()

    create_nest_folder("./data/item_data")
    # get detail information of items
    # save result to file ./item_data/[shop_id]_[item_id].json
    craw_item_details()

    create_nest_folder("./data/shop_data")
    # get detail information of shop
    # save result to file ./shop_data/[shop_id].json
    craw_shop_details()
