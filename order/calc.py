import pymongo

dbs = pymongo.MongoClient(
    'mongodb://root:password123@18.140.157.75:27018/?authSource=admin&ssl=false&directConnection=true')
c_orders = dbs['baobab'].orders
c_event_trans = dbs['baobab'].event_transactions


order_ids = c_event_trans.distinct("order_id")

# In danh sách order_id
print(order_ids)
