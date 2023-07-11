import json
import streamlit as st
import pandas as pd
from io import BytesIO

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
st.dataframe(data, height=500)

# 创建一个下载按钮，将DataFrame导出为Excel文件
def download_excel():
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    data.to_excel(writer, sheet_name='Result', index=False)
    writer.save()
    processed_data = output.getvalue()
    return processed_data

button = st.download_button(
    label='Download Excel',
    data=download_excel(),
    file_name='result.xlsx',
    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
)