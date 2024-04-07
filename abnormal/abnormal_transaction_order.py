from pymongo import MongoClient
import pandas as pd
# Kết nối đến database MongoDB
client = MongoClient("mongodb://root:password123@18.140.157.75:27018/?authSource=admin&ssl=false&directConnection=true")
db = client["baobab_20240317"]

# Lấy collection orders và transactions
orders_collection = db["orders"]
transactions_collection = db["transactions"]

# Sử dụng $lookup để kết hợp dữ liệu từ hai collection dựa trên trường order_id
pipeline = [
    {
        "$lookup": {
            "from": "transactions",
            "localField": "_id",
            "foreignField": "order",
            "as": "transactions_data",
        }
    },
    # {
    #     "$match": {
    #         "transactions_data.amount": {"$ne": "$total"},
    #     }
    # },
    {
        "$project": {
            "_id": 1,
            "total": 1,
            "transactions_data.amount": 1,
        }
    },
    {
        "$sort": {"total": -1},
    },
]

# Thực hiện truy vấn và lấy kết quả
results = orders_collection.aggregate(pipeline)
count = 0
# Duyệt qua kết quả
json_data = []
for order in results:
    if len(order['transactions_data']) != 0 and order['total'] != order['transactions_data'][0]['amount']:
        count += 1
        order['id'] = str(order['_id'])

        order['price_order'] = order['total']
        order['price_transaction'] = order['transactions_data'][0]['amount']
        order['diff'] = abs(order['price_order'] - order['price_transaction'])
        del order['_id']
        del order['transactions_data']
        del order['total']
        json_data.append(order)
        # Json to DataFrame

df = pd.json_normalize(json_data)

# DataFrame to Excel
excel_filename = 'data.xlsx'
df.to_excel(excel_filename, index=False)
