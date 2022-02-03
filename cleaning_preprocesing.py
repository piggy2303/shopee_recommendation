import json
import pandas as pd
import numpy as np
import os
# import matplotlib.pyplot as plt
import re
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()


def preprprocess_string(a: str) -> str:
    a = a.lower().replace("\n", " ")

    s1 = u'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ'
    s0 = u'AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYy'
    s = ''

    for c in a:
        if c in s1:
            s += s0[s1.index(c)]
        else:
            s += c

    s = re.sub('[^A-Z a-z0-9]+', '', s)
    return s


def item_json_to_object(json_file_path: str) -> dict:
    shopid = json_file_path.split("_")[0]
    itemid = json_file_path.split("_")[1].split(".")[0]

    item_details = open("item_data/"+json_file_path, "r")
    item_details = json.load(item_details)
    item_name = preprprocess_string(item_details["name"])
    item_price = item_details["price"]
    item_rating = item_details["item_rating"]["rating_star"]
    item_sold = item_details["historical_sold"]
    item_category = []

    for i in item_details["categories"]:
        item_category.append(int(i["catid"]))

    # categories is an array of int > 0
    # len of this array is from 2 to 4
    # so adding 0 to the null value
    if len(item_category) == 2:
        item_category.append(0)
        item_category.append(0)
    if len(item_category) == 3:
        item_category.append(0)

    item_ctime = item_details["ctime"]
    item_brand_id = item_details["brand_id"]
    item_comment_count = item_details["cmt_count"]

    return({
        "item_id": int(itemid),
        "shopid": int(shopid),
        "item_name": item_name,
        "item_price": int(item_price/10000000),
        "item_rating": item_rating,
        "item_sold": int(item_sold),
        "cat_0": item_category[0],
        "cat_1": item_category[1],
        "cat_2": item_category[2],
        "cat_3": item_category[3],
        "item_ctime": int(item_ctime),
        "item_brand_id": int(item_brand_id),
        "item_comment_count": int(item_comment_count),
    })


def shop_json_to_object(json_file_path: str) -> dict:
    shopid = json_file_path.split('.')[0]

    shop_details = open("shop_data/"+json_file_path, "r")
    shop_details = json.load(shop_details)

    shop_slug = shop_details["account"]["username"]
    rating_star = shop_details["rating_star"]
    response_rate = shop_details["response_rate"]
    response_time = shop_details["response_time"]
    follower_count = shop_details["follower_count"]
    rating_bad = shop_details["rating_bad"]
    rating_good = shop_details["rating_good"]
    rating_normal = shop_details["rating_normal"]
    item_count = shop_details["item_count"]

    return({
        "shopid": int(shopid),
        "shop_slug": shop_slug,
        "rating_star": rating_star,
        "response_rate": response_rate,
        "response_time": response_time,
        "follower_count": follower_count,
        "rating_bad": rating_bad,
        "rating_good": rating_good,
        "rating_normal": rating_normal,
        "item_count": item_count
    })


def preprprocess_item():
    item_data = []
    for i in os.listdir("item_data/"):
        item_data.append(item_json_to_object(i))

    item_data = pd.DataFrame(item_data)
    item_data.to_pickle("item_data.pkl")
    print("save item_data")


def calculate_score(shop_data: pd.DataFrame) -> np.array:
    shop_x = shop_data[['rating_star', 'response_rate',
                        'response_time', 'follower_count',
                        'rating_bad', 'rating_good',
                        'rating_normal', 'item_count']]
    shop_x = scaler.fit_transform(shop_x)

    m1 = shop_x
    m2 = np.array([
        [4],    # rating_star
        [1],    # response_rate
        [-1],   # response_time
        [3],    # follower_count
        [-3],   # rating_bad
        [3],    # rating_good
        [1],    # rating_normal
        [0.5]   # item_count
    ])
    m3 = np.dot(m1, m2)
    m3 = scaler.fit_transform(m3)
    m3 = m3.reshape(m3.shape[0],)
    return m3


def preprprocess_shop():
    shop_data = []
    for i in os.listdir("shop_data/"):
        shop_data.append(shop_json_to_object(i))
    shop_data = pd.DataFrame(shop_data)

    # fillna in dataframe
    shop_data["rating_star"].fillna(
        shop_data['rating_star'].min(), inplace=True)
    shop_data["response_rate"].fillna(
        shop_data['response_rate'].min(), inplace=True)
    shop_data["response_time"].fillna(
        shop_data['response_time'].min(), inplace=True)
    shop_data["follower_count"].fillna(
        shop_data['follower_count'].min(), inplace=True)
    shop_data["rating_bad"].fillna(shop_data['rating_bad'].min(), inplace=True)
    shop_data["rating_good"].fillna(
        shop_data['rating_good'].min(), inplace=True)
    shop_data["rating_normal"].fillna(
        shop_data['rating_normal'].min(), inplace=True)
    shop_data["item_count"].fillna(shop_data['item_count'].min(), inplace=True)

    # calculate shop score
    shop_score = shop_data[["shopid", "shop_slug"]]
    shop_score["shop_score"] = calculate_score(shop_data)
    shop_score = shop_score.sort_values(by="shop_score", ascending=False)

    # now notice the last row have score = 0 because minmaxscaler
    # we don't want score = 0 because after that this score will multiply with the weight
    # so we need to change meet the condition
    # average(row[-1] + row[-3]) == row[-2]
    # if row[-1] < 0 then row[-1] = row[-2] / 2
    a_1 = shop_score.iloc[-1]["shop_score"]
    a_2 = shop_score.iloc[-2]["shop_score"]
    a_3 = shop_score.iloc[-3]["shop_score"]

    a_1 = 2*a_2 - a_3
    if a_1 <= 0:
        a_1 = a_2/2

    shop_score = shop_score.replace(0, a_1)
    print(shop_score)

    shop_score.to_pickle("shop_data.pkl")
    print("save shop_data")


if __name__ == "__main__":
    preprprocess_item()
    preprprocess_shop()
