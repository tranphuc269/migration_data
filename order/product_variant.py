import pymongo
from bson import ObjectId

from env import MONGO_URL

dbs = pymongo.MongoClient(
    'mongodb://root:password123@18.140.157.75:27018/?authSource=admin&ssl=false&directConnection=true')

collection = dbs['teaology'].orders
for document in collection.find({}):
    print("Bắt đầu sửa đổi dữ liệu - {}".format(str(document['_id'])))
    # copy product_variants -> tmp_product_variants
    product_variants = document['product_variants']
    service_type = document['service_type']
    price_key = (
        "price"
        if service_type == 0
        else "dinein_price"
    )
    update_tmp_product_variants = {
        "$set":
            {"tmp_product_variants": product_variants}
    }
    print("Sao chép col mới :: tmp_product_variants - {}".format(str(document['_id'])))
    x = collection.update_one({'_id': document['_id']}, update_tmp_product_variants)
    print(x.modified_count, "documents updated.")
    # change data product variants
    new_product_variants = []
    for product_variant in product_variants:
        price_include_addon = product_variant['price_final'] / product_variant['number']
        product_variant['price_final'] = price_include_addon
        for addon_variant in product_variant['addon_variants']:
            for order_option in addon_variant['order_options']:
                price_include_addon += order_option[price_key]
        product_variant['price_final_include_addon'] = price_include_addon
        product_variant['total_price_of_product'] = price_include_addon * product_variant['number']
        new_product_variants.append(product_variant)
    print(new_product_variants)
    update_product_variants = {
        "$set":
            {"product_variants": new_product_variants}
    }
    collection.update_one({'_id': document['_id']}, update_product_variants)
    print("Cập nhật lại dữ liệu :: product_variants của bản ghi  - {}".format(str(document['_id'])))
    print("Kết thúc sửa đổi dữ liệu - {}".format(str(document['_id'])))
