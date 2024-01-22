import pymongo

dbs = pymongo.MongoClient(
    'mongodb://root:password123@18.140.157.75:27018/?authSource=admin&ssl=false&directConnection=true')
collection = dbs['baobab'].orders
for document in collection.find({}):
    if document['payment_method'] == 1 or document['payment_method'] == 10 or document['payment_method'] == 5 or \
            document['payment_method'] == 3:
        document['payment_provider'] = 1
        collection.update_one({'_id': document['_id']}, {
            "$set":
                {"payment_provider": 1}
        })
    if document['payment_method'] == 0:
        document['payment_provider'] = 0
        collection.update_one({'_id': document['_id']}, {
            "$set":
                {"payment_provider": 0}
        })
