from time import sleep

from helpers import parse_meebit_data, parse_sale_data
import requests
import pandas as pd

import pymongo
from pymongo import MongoClient

import matplotlib
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(layout="wide")
st.title('Data mining Meebits NFTs')
st.markdown("""
Data mining Meebits NFTs using Python and OpenSea API!
""")

plt.style.use('ggplot')

client = MongoClient()
db = client.meebitsDB
meebits_collection = db.meebitsCollection
sales_collection = db.salesCollection

meebits = meebits_collection.find()
meebits_df = pd.DataFrame(meebits)

meebit_sales = sales_collection.find()
meebit_sales_df = pd.DataFrame(meebit_sales)

print("The database has information about %d Meebits." % len(meebits_df))
print("The database has information about %d Meebits sale transactions." % len(meebit_sales_df))

creators = []
for creator_address in meebits_df['creator_address'].value_counts().index[:10]:
    creator_data = {}
    creator_data['creator_address'] = creator_address
    creator_data['creator_username'] = meebits_df[meebits_df['creator_address'] == creator_address]['creator_username'].iloc[0]
    creator_data['number_meebits'] = len(meebits_df[meebits_df['creator_address'] == creator_address])
    creators.append(creator_data)

st.dataframe(pd.DataFrame(creators))

#### Getting total number of Meebit Creators and Owners.
print("There are %d unique Meebit creators." % len(meebits_df['creator_address'].unique()))
print("There are %d unique Meebit owners." % len(meebits_df['owner_address'].unique()))

buyers = []
for buyer_address in meebit_sales_df['buyer_address'].value_counts().index[:10]:
    buyer_data = {}
    buyer_data['buyer_address'] = buyer_address
    buyer_data['buyer_username'] = \
    meebit_sales_df[meebit_sales_df['buyer_address'] == buyer_address]['buyer_username'].iloc[0]
    buyer_data['number_buys'] = len(meebit_sales_df[meebit_sales_df['buyer_address'] == buyer_address])
    buyer_data['min_price'] = meebit_sales_df[meebit_sales_df['buyer_address'] == buyer_address]['total_price'].min()
    buyer_data['max_price'] = meebit_sales_df[meebit_sales_df['buyer_address'] == buyer_address]['total_price'].max()
    buyer_data['mean_price'] = meebit_sales_df[meebit_sales_df['buyer_address'] == buyer_address]['total_price'].mean()
    buyers.append(buyer_data)

st.dataframe(pd.DataFrame(buyers))

sellers = []
for seller_address in meebit_sales_df['seller_address'].value_counts().index[:10]:
    seller_data = {}
    seller_data['seller_address'] = seller_address
    seller_data['seller_username'] = \
    meebit_sales_df[meebit_sales_df['seller_address'] == seller_address]['seller_username'].iloc[0]
    seller_data['number_sales'] = len(meebit_sales_df[meebit_sales_df['seller_address'] == seller_address])
    seller_data['min_price'] = meebit_sales_df[meebit_sales_df['seller_address'] == seller_address]['total_price'].min()
    seller_data['max_price'] = meebit_sales_df[meebit_sales_df['seller_address'] == seller_address]['total_price'].max()
    seller_data['mean_price'] = meebit_sales_df[meebit_sales_df['seller_address'] == seller_address][
        'total_price'].mean()
    sellers.append(seller_data)

st.dataframe(pd.DataFrame(sellers))

