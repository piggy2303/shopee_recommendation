<h1> Recommendation System</h1>

# 1. Quick start

You need Docker and Docker-compose to run the following command

    bash start.sh

# 2. Manual running

## 2.1 Crawling data

You can choose "Manual crawling" or "Download data from gg drive"

### 2.1.1 Manual crawling

Use real shopee data. Get the list of shops of shopee mall

Only use shop from this link [electronics category](https://shopee.vn/mall/brands/11036132)

Run file crawl_data.py to crawl detailed information of shop and items.

    python3 crawl_data.py

The output will be stored in the folder: [raw_data](./raw_data), [item_data](./item_data), [shop_data](./shop_data)

For more information about how to crawl_data, please see file [crawl_data.py](crawl_data.py)

### 2.1.2 Download data from gg drive

If you don't want to waste time crawling data

Please download it from [this link](https://drive.google.com/file/d/1HJJ06peMHtdzIGaEvc8bU61XE3ZjpBUL/view?usp=sharing)

Unzip it and place the "data" folder in the project

## 2.2 Cleaning and preprocessing data

Run file cleaning_preprocesing.py to clean and preprocess data.

    python3 cleaning_preprocessing.py

The output of item detail data will be stored in the file: [item_data.pkl](item_data.pkl)

The output of shop detail data will be stored in the file: [shop_data.pkl](shop_data.pkl)

For more information about how to clean and preprocess data, please see file [cleaning_preprocesing.ipynb](cleaning_preprocesing.ipynb)

## 2.3 Recommendation

Prepare input file [input.txt](input.txt). Copy link of item to this file.
Each line is an item link.

Because I only crawl data from the electronics category, this code only recommended shop for the items of the electronics category. Example

    https://shopee.vn/item_a
    https://shopee.vn/item_b
    https://shopee.vn/item_c

Run file recommendedation.py to get Recommendation output

    python3 recommendedation.py

Output is the top 3 links to shop recommended for you from the list of items you pick from the input file. Data will be stored in the
[output.txt](output.txt). Example

    https://shopee.vn/shop_a
    https://shopee.vn/shop_b
    https://shopee.vn/shop_c

For more information about how this algorithm works, please see file [recommendation.ipynb](recommendation.ipynb)
