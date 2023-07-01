import json
import streamlit as st
import pandas as pd

# 读取recipes.json文件
with open('recipes.json', 'r') as f:
    recipes = json.load(f)

# 创建一个空的DataFrame
data = pd.DataFrame(columns=['Level', 'Essence', 'Rarity', 'Amount Needed', 'Amount Owned', 'Remaining Amount'])

# 让用户录入inventories的数据
st.write('Please enter your inventories data:')
inventories = st.text_area('Inventories Data', value='{"items":[], "essences": []}', height=200)
inventories_dict = json.loads(inventories)
essences = inventories_dict["essences"]

# 计算每个等级还差哪些物品和数量，并添加到DataFrame中
for level in recipes:
    level_shown = False
    for recipe in recipes[level]:
        item_name = recipe['name']
        item_rarity = recipe['rarity']
        item_amount = recipe['amount']
        owned_amount = 0
        for essence in essences:
            if essence['name'] == item_name and essence['rarity'] == item_rarity:
                owned_amount += essence['amount']
        if owned_amount < item_amount:
            if not level_shown:
                data = data.append({
                    'Level': level,
                    'Essence': item_name,
                    'Rarity': item_rarity,
                    'Amount Needed': item_amount,
                    'Amount Owned': owned_amount,
                    'Remaining Amount': int(item_amount - owned_amount) if (item_amount - owned_amount) > 0 else 0
                }, ignore_index=True)
                level_shown = True
            else:
                data = data.append({
                    'Level': '',
                    'Essence': item_name,
                    'Rarity': item_rarity,
                    'Amount Needed': item_amount,
                    'Amount Owned': owned_amount,
                    'Remaining Amount': int(item_amount - owned_amount) if (item_amount - owned_amount) > 0 else 0
                }, ignore_index=True)

# 在网站上展示DataFrame
st.write('Result:')
st.write(data)