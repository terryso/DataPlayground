'''
title           : helpers.py
description     : Helper functions used for parsing the outcome of OpenSea APIs.
author          : Adil Moujahid
date_created    : 20210627
date_modified   : 20210627
version         : 1.0
python_version  : 3.6.8
'''
from time import sleep

import requests


def parse_meebit_data(meebit_dict):
    meebit_id = meebit_dict['token_id']

    try:
        creator_username = meebit_dict['creator']['user']['username']
    except:
        creator_username = None
    try:
        creator_address = meebit_dict['creator']['address']
    except:
        creator_address = None

    try:
        owner_username = meebit_dict['owner']['user']['username']
    except:
        owner_username = None

    owner_address = meebit_dict['owner']['address']

    traits = meebit_dict['traits']
    num_sales = int(meebit_dict['num_sales'])

    result = {'meebit_id': meebit_id,
              'creator_username': creator_username,
              'creator_address': creator_address,
              'owner_username': owner_username,
              'owner_address': owner_address,
              'traits': traits,
              'num_sales': num_sales}

    return result


def parse_sale_data(sale_dict):
    is_bundle = False

    if sale_dict['asset'] is not None:
        meebit_id = sale_dict['asset']['token_id']
    elif sale_dict['asset_bundle'] is not None:
        meebit_id = [asset['token_id'] for asset in sale_dict['asset_bundle']['assets']]
        is_bundle = True

    seller_address = sale_dict['seller']['address']
    buyer_address = sale_dict['winner_account']['address']

    try:
        seller_username = sale_dict['seller']['user']['username']
    except:
        seller_username = None
    try:
        buyer_username = sale_dict['winner_account']['user']['username']
    except:
        buyer_username = None

    timestamp = sale_dict['transaction']['timestamp']
    total_price = float(sale_dict['total_price'])
    payment_token = sale_dict['payment_token']['symbol']
    usd_price = float(sale_dict['payment_token']['usd_price'])
    transaction_hash = sale_dict['transaction']['transaction_hash']

    result = {'is_bundle': is_bundle,
              'meebit_id': meebit_id,
              'seller_address': seller_address,
              'buyer_address': buyer_address,
              'buyer_username': buyer_username,
              'seller_username': seller_username,
              'timestamp': timestamp,
              'total_price': total_price,
              'payment_token': payment_token,
              'usd_price': usd_price,
              'transaction_hash': transaction_hash}

    return result


def get_assets_data(address, collection):
    url = "https://api.opensea.io/api/v1/assets"

    for i in range(0, 1000):
        querystring = {"token_ids": list(range((i * 20) + 1, (i * 20) + 21)),
                       "asset_contract_address": address,
                       "order_direction": "desc",
                       "offset": "0",
                       "limit": "20"}
        print(f'querystring: {querystring}')
        response = requests.request("GET", url, params=querystring, verify=False)
        print(f'response: {response.json()}')

        print(i, end=" ")
        if response.status_code != 200:
            print('error')
            break

        # Getting meebits data
        meebits = response.json()['assets']
        # Parsing meebits data
        parsed_meebits = [parse_meebit_data(meebit) for meebit in meebits]
        # storing parsed meebits data into MongoDB
        collection.insert_many(parsed_meebits)

        sleep(2)


def get_sale_transactions_data(address, collection):
    url = "https://api.opensea.io/api/v1/events"

    for i in range(0, 100):

        querystring = {"asset_contract_address": address,
                       "event_type": "successful",
                       "only_opensea": "true",
                       "offset": i * 50,
                       "limit": "50"}

        headers = {"Accept": "application/json"}

        response = requests.request("GET", url, headers=headers, params=querystring)
        print(f'response: {response.json()}')

        print(i, end=" ")
        if response.status_code != 200:
            print('error')
            break

        # Getting meebits sales data
        meebit_sales = response.json()['asset_events']

        if meebit_sales == []:
            break

        # Parsing meebits sales data
        parsed_meebit_sales = [parse_sale_data(sale) for sale in meebit_sales]
        # storing parsed meebits data into MongoDB
        collection.insert_many(parsed_meebit_sales)

        sleep(2)
