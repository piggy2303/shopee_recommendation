import json
from re import S
import pandas as pd
import numpy as np
import os
import time
# import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from pandas.core.common import SettingWithCopyWarning
import warnings
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)


# constatnt
item_data = pd.read_pickle("item_data.pkl")
shop_data = pd.read_pickle("shop_data.pkl")
columns_get_score = ['item_rating',
                     'item_sold',
                     'item_comment_count',
                     'price_diff',
                     'jaccard_name',
                     'ctime_diff']


def jaccard_similarity(a, b):
    a = set(a.split(" "))
    b = set(b.split(" "))
    j = float(len(a.intersection(b))) / len(a.union(b))
    return j


def get_random_item(df: pd.DataFrame) -> pd.DataFrame:
    random_index = np.random.randint(0, len(item_data))
    print("random_index", random_index)
    item_pick = df.loc[[random_index]]

    print("link item_input : https://shopee.vn/-cLHC4151-i." +
          str(item_pick["shopid"].values[0])+"."+str(item_pick["item_id"].values[0]))
    return item_pick


def filter_data_by_categories(df: pd.DataFrame, df_input) -> pd.DataFrame:
    df_new = df[df['shopid'] != df_input['shopid'].values[0]]

    if df_input["cat_2"].values[0] == 0:
        df_new = df_new[df_new['cat_1'] == df_input['cat_1'].values[0]]
    else:
        df_new = df_new[df_new['cat_2'] == df_input['cat_2'].values[0]]

    if df_new.empty:
        print("empty DataFrame")
        df_new = df[df['cat_0'] == df_input['cat_0'].values[0]]
        df_new = df_new.sample(n=30, random_state=1)

    return df_new


def create_data_for_scoring(item_recomd: pd.DataFrame,
                            item_pick: pd.DataFrame,
                            columns_get_score: list) -> pd.DataFrame:
    time_now = int(time.time())
    scaler = MinMaxScaler()

    item_recomd["price_diff"] = item_recomd['item_price'].apply(
        lambda x: abs(x - item_pick['item_price'].values[0]))
    item_recomd["jaccard_name"] = item_recomd['item_name'].apply(
        lambda x: jaccard_similarity(item_pick['item_name'].values[0], x))
    item_recomd["ctime_diff"] = item_recomd['item_ctime'].apply(
        lambda x: time_now - x)

    item_x = item_recomd.drop(
        ["item_brand_id", "item_ctime", 'item_price', 'cat_0', 'cat_1', 'cat_2', 'cat_3'], axis=1)
    item_x[columns_get_score] = scaler.fit_transform(item_x[columns_get_score])

    return item_x


def calculate_score_for_item(item_x: pd.DataFrame, columns_get_score: list) -> pd.DataFrame:
    m1 = np.array(item_x[columns_get_score])
    m2 = np.array([
        [2],  # item_rating
        [1],  # item_sold
        [1],  # item_comment_count
        [-3],  # price_diff
        [8],  # jaccard_name
        [-2]]  # ctime_diff
    )
    m3 = np.dot(m1, m2)
    m3 = m3.reshape(m3.shape[0],)
    return m3


def shop_score_weight(item_x: pd.DataFrame) -> pd.DataFrame:
    n = len(item_x)
    x = np.arange(0, n)
    y = np.power(0.9, x)

    item_x["weight"] = y
    item_x["shop_score_weight"] = item_x["shop_score"] * item_x["weight"]

    item_x = item_x.groupby(['shop_slug'])[
        'shop_score_weight'].agg('sum').reset_index()

    return item_x


def get_item_id_from_link(item_link: str) -> int:
    try:
        item_link = item_link.split("?")[0]
        item_id = item_link.split(".")[-1]
        shopid = item_link.split(".")[-2]
        print("iterm_id ", item_id, " shopid", shopid)
        return int(item_id)
    except:
        print("not found item_id")
        return None


def recommendations_from_one(item_link: str = None):
    if item_link is None:
        item_pick = get_random_item(item_data)
    else:
        item_id = get_item_id_from_link(item_link)
        if item_id is None:
            return None

        item_pick = item_data[item_data['item_id'] == item_id]

    if item_pick.empty:
        return None

    item_recomd = filter_data_by_categories(item_data, item_pick)
    item_recomd = create_data_for_scoring(item_recomd,
                                          item_pick,
                                          columns_get_score)
    item_recomd["score"] = calculate_score_for_item(item_recomd,
                                                    columns_get_score)
    item_recomd = item_recomd.sort_values(
        by=['score'], ascending=False).head(50)

    item_recomd = item_recomd.drop(["item_id",
                                    'item_name',
                                    'item_rating',
                                    'item_sold',
                                    'item_comment_count',
                                    'price_diff',
                                    'jaccard_name',
                                    'ctime_diff'], axis=1)

    item_recomd = item_recomd.merge(
        shop_data, on='shopid', how='left')
    item_recomd = shop_score_weight(item_recomd)
    return item_recomd


def summarizing_recomd(list_input: list) -> list:
    results = []
    for item_link in list_input:
        item_recomd = recommendations_from_one(item_link)
        if item_recomd is not None:
            results.append(item_recomd)
    final_result = pd.concat(results)

    final_result = final_result.groupby(
        ['shop_slug'])['shop_score_weight'].agg('sum').reset_index()
    final_result = final_result.sort_values(by=['shop_score_weight'],
                                            ascending=False).head(3)

    final_result = final_result["shop_slug"].tolist()

    final_result = ["https://shopee.vn/" + i for i in final_result]

    return final_result


if __name__ == "__main__":
    file_input = open("input.txt", "r")

    list_input = []
    for line in file_input:
        line = line.strip()
        print(line)
        list_input.append(line)
    file_input.close()

    list_output = summarizing_recomd(list_input)
    print(list_output)
    file_output = open("output.txt", "w")
    for line in list_output:
        file_output.write(line + "\n")

    file_output.close()
