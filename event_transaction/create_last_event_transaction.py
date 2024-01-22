import datetime
import time
from enum import Enum
import pymongo
from bson import ObjectId


class TRANS_TYPE(Enum):
    SALE = 0
    REFUND = 1


class PAYMENT_TRANS_TYPE(Enum):
    CASH = 0
    CARD = 1
    VIPPS = 2


class PAYMENT_METHOD(Enum):
    CASH = 0
    VIPPS_EPAY = 1
    VIPPS_QR = 2
    NETS_EPAY = 3
    VIPPS_CARD = 4
    NETS_BANK_TERMINAL = 5
    VERIFONE_BANK_TERMINAL = 6
    NETS_EXTERNAL_BANK_TERMINAL = 7
    VERIFONE_EXTERNAL_BANK_TERMINAL = 8
    DINTERO = 9
    NETS_EASY = 10


dbs = pymongo.MongoClient(
    'mongodb://root:password123@18.140.157.75:27018/?authSource=admin&ssl=false&directConnection=true')

c_order = dbs['baobab'].orders
c_event_transaction = dbs['baobab'].event_transactions
for document in c_order.find({}):
    print('Dữ liệu document convert :: {}'.format(document))
    if "payment_provider" in document:
        event_trans_data = {
            'shop_id': ObjectId(document['shop_id']),
            'order_id': document['_id'],
            'trans_type': -1,
            # 'trans_time': datetime.datetime.fromtimestamp(document['created_at']) is isinstance(document['created_at'],
            #                                                                                     float) else document[
            # 'created_at'],
            'payment_type': -1,
            'payment_provider': document['payment_provider'],
            'payment_provider_option': document['payment_method'],
        }
        if document['payment_method'] == PAYMENT_METHOD.VIPPS_EPAY.value or \
                document['payment_method'] == PAYMENT_METHOD.VIPPS_QR.value:
            event_trans_data['payment_type'] = PAYMENT_TRANS_TYPE.VIPPS.value
        elif document['payment_method'] == PAYMENT_METHOD.CASH.value:
            event_trans_data['payment_type'] = PAYMENT_TRANS_TYPE.CASH.value
        else:
            event_trans_data['payment_type'] = PAYMENT_TRANS_TYPE.CARD.value
        if document['payment_status'] == 3:
            # insert payment success before insert payment refund
            event_trans_data['trans_type'] = 0
            if isinstance(document['created_at'], float):
                event_trans_data['trans_time'] = datetime.datetime.fromtimestamp(document['created_at'] / 1000)
            else:
                event_trans_data['trans_time'] = document['created_at']
            print('Dữ liệu event transaction success trước khi refund insert :: {}'.format(event_trans_data))
            _before_refund_data = event_trans_data.copy()
            _before_refund_data['_id'] = ObjectId()
            data = c_event_transaction.insert_one(_before_refund_data)
            print('Đã thêm dữ liệu trước khi refund :: {}'.format(data.inserted_id))

            event_trans_data['trans_type'] = 1
            time.sleep(1)
        if document['payment_status'] == 1:
            event_trans_data['trans_type'] = 0

        if event_trans_data['trans_type'] != -1:

            if isinstance(document['created_at'], float):
                event_trans_data['trans_time'] = datetime.datetime.fromtimestamp(document['created_at'] / 1000)
            else:
                event_trans_data['trans_time'] = document['created_at']

            print('Dữ liệu event transaction insert :: {}'.format(event_trans_data))
            data = c_event_transaction.insert_one(event_trans_data)
            time.sleep(1)
            print('Đã thêm dữ liệu :: {}'.format(data.inserted_id))
        else:
            print('Dữ liệu không thể tạo transaction event')
        print('======================================')
        time.sleep(1)
