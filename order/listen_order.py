import pymongo

dbs = pymongo.MongoClient(
    'mongodb://root:password123@18.140.157.75:27018/?authSource=admin&ssl=false&directConnection=true')

db = dbs['teaology']
coll = db['orders']
with coll.watch([{'$match': {'operationType': 'insert'}}]) as change_stream:
    for insert_change in change_stream:
        print(insert_change)
        # inserted_entry = insert_change['fullDocument']
        # if 'category' not in inserted_entry.keys():
        #     coll.update_one(inserted_entry,{"$set":{"category":"None"}})
