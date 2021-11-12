import pymongo
from django.http import HttpResponse, JsonResponse
import json
from .redis import redis_connection
import random
from uuid import uuid4 as uuid

myclient = pymongo.MongoClient("mongodb://mongodb:27017/")
mydb = myclient["mydatabase"]
customers = mydb["customers"]

customers_amount = 2000
fields_amount = 30
redis_ttl = 30
cache_flushing_threshold_ttl = 15


def update_random_user(request):
    random_data = {f'field_{i}': str(uuid()) for i in range(fields_amount)}
    customers.update_one({'cust_id': f"{random.randint(0, customers_amount)}"}, {"$set": random_data}, upsert=True)
    return HttpResponse('')


def create_all_users(request):
    for i in range(customers_amount):
        random_data = {f'field_{i}': str(uuid()) for i in range(fields_amount)}
        customers.update_one({'cust_id': f"{i}"}, {"$set": random_data}, upsert=True)
    return HttpResponse('')


def get_random_user(request):
    customer_random_id = random.randint(0, customers_amount-1)
    # redis_customer_encoded = redis_connection.get(customer_random_id)
    # if redis_customer_encoded:
    #     ttl = redis_connection.pttl(customer_random_id) / 1000
    #     if not should_flush_cache(ttl, cache_flushing_threshold_ttl):
    #         pass
    #     redis_customer = redis_customer_encoded.decode()
    #     customer = json.loads(redis_customer)
    #     return JsonResponse(customer)

    customer = customers.find_one({"cust_id": f"{customer_random_id}"})
    customer.pop('_id')
    # customer_string = json.dumps(customer)
    # redis_connection.setex(customer_random_id, redis_ttl, customer_string)
    return JsonResponse(customer)


def should_flush_cache(ttl, threshold_ttl):
    return ttl < threshold_ttl and random.random() < (
        (threshold_ttl - ttl) / threshold_ttl
    )