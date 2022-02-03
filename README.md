<h1> Recommendation System</h1>

# 1. Quick start

You need Docker and Docker-compose to run the following command

    bash start.sh

# 2. Manual runing

## 2.1 Crawling data

Use real shopee data. Get the list of shops of shopee mall

Only use shop from this link [electronics category](https://shopee.vn/mall/brands/11036132)

Run file crawl_data.py to crawl details infomation of shop and items.

    python3 crawl_data.py

Output will be stored in the folder: [raw_data](./raw_data), [item_data](./item_data), [shop_data](./shop_data)

For more information about how to crawl_data please see file [crawl_data.py](crawl_data.py)

## 2.2 Cleaning and preprocesing data

Run file cleaning_preprocesing.py to cleaning and preprocesing data.

    python3 cleaning_preprocesing.py

Output of item detail data will be stored in the file: [item_data.pkl](item_data.pkl)

Output of shop detail data will be stored in the file: [shop_data.pkl](shop_data.pkl)

For more information about how to cleaning and preprocesing data please see file [cleaning_preprocesing.ipynb](cleaning_preprocesing.ipynb)

## 2.3 Recommendation

Prepare input file [input.txt](input.txt). Copy link of item to this file.
Each line is an item link.

Because i only crawl data from [electronics category](https://shopee.vn/mall/brands/11036132) so this code only recommended shop for the items of electronics category. Example

    https://shopee.vn/item_a
    https://shopee.vn/item_b
    https://shopee.vn/item_c

Run file recommendedation.py to get Recommendation output

    python3 recommendedation.py

Output is the top 3 link to shop that is recommended for you from list of item you pick from input file . Data will be stored in the [output.txt](output.txt). Example

    https://shopee.vn/shop_a
    https://shopee.vn/shop_b
    https://shopee.vn/shop_c

For more information about how this algorithm wroking please see file [recommendation.ipynb](recommendation.ipynb)
