import pymongo
from pprint import pprint
import secrets
from mongo_queue.queue import Queue
import time
import string
import random


client = pymongo.MongoClient("mongodb+srv://dbUser:qwep-]123p=]@cluster0-ifgr4.mongodb.net/Cluster0?retryWrites=true&w=majority")


def user_exist(username, password):
    data = client.users.usernames.find_one({
        'username': username,
        'password': password
    })
    if data is None:
        return (False,)
    data.pop("_id")
    data.pop("password")
    return True, data


def clear_queue():
    client.update_queue_db.update_queue.delete_many({})
    client.update_queue_db.job_ids.delete_many({})


def get_session(uid):
    return client.sessions_data.sessions_active.find_one({
        "uid": uid
    })


def init_session(uid):
    client.sessions_data.sessions_active.insert_one({
        "uid": uid,
        "users": {},
        "order": [],
        "cur_pos": 1,
        "active": "dashboard",
        "tab": "visible"
    })


def modify_session(uid, data):
    client.sessions_data.sessions_active.update_one({
        "uid": uid
    }, {"$set": data})


def delete_session(uid):
    client.sessions_data.sessions_active.delete_one({
        "uid": uid
    })


def mark_pending(job_id):
    client.update_queue_db.job_ids.insert_one({
        "job_id": job_id
    })


def mark_done(job_id):
    client.update_queue_db.job_ids.delete_one({
        "job_id": job_id
    })


def check_job(job_id):
    return client.update_queue_db.job_ids.find_one({
        "job_id": job_id
    }) is None


def get_items(api_key, client_id):
    return client.ozon_data.items.find_one({
        "creds": f"{api_key}:{client_id}"
    })


def get_postings(api_key, client_id):
    return client.ozon_data.postings.find_one({
        "creds": f"{api_key}:{client_id}"
    })


#mark_done("job1234")


def insert_deliver_job(api_key, client_id, posting_numbers, job_id):
    queue = Queue(client.update_queue_db.update_queue, consumer_id=''.join(random.choice(string.ascii_lowercase) for i in range(10)), timeout=300, max_attempts=3)
    queue.put({"api_key": api_key, "client_id": client_id, "posting_numbers": posting_numbers,  "job_id": job_id}, channel="deliver_queue")
    mark_pending(job_id)


def insert_items_update_job(api_key, client_id, job_id):
    queue = Queue(client.update_queue_db.update_queue, consumer_id=''.join(random.choice(string.ascii_lowercase) for i in range(10)), timeout=300, max_attempts=3)
    queue.put({"api_key": api_key, "client_id": client_id, "job_id": job_id}, channel="items_priority")
    mark_pending(job_id)


def insert_items_regular_update(api_key, client_id, job_id):
    queue = Queue(client.update_queue_db.update_queue, consumer_id=''.join(random.choice(string.ascii_lowercase) for i in range(10)), timeout=300, max_attempts=3)
    queue.put({"api_key": api_key, "client_id": client_id, "job_id": job_id}, channel="items_queue")
    mark_pending(job_id)


def insert_postings_update_job(api_key, client_id, job_id):
    queue = Queue(client.update_queue_db.update_queue, consumer_id=''.join(random.choice(string.ascii_lowercase) for i in range(10)), timeout=300, max_attempts=3)
    queue.put({"api_key": api_key, "client_id": client_id, "job_id": job_id}, channel="postings_priority")
    mark_pending(job_id)
    print("INSERTED")


def insert_postings_regular_update(api_key, client_id, job_id):
    queue = Queue(client.update_queue_db.update_queue, consumer_id=''.join(random.choice(string.ascii_lowercase) for i in range(10)), timeout=300, max_attempts=3)
    queue.put({"api_key": api_key, "client_id": client_id, "job_id": job_id}, channel="postings_queue")
    mark_pending(job_id)


def insert_act_job(api_key, client_id, job_id):
    queue = Queue(client.update_queue_db.update_queue, consumer_id=''.join(random.choice(string.ascii_lowercase) for i in range(10)), timeout=300, max_attempts=3)
    queue.put({"api_key": api_key, "client_id": client_id, "job_id": job_id}, channel="act_queue")
    mark_pending(job_id)


def get_items_ids(api_key, client_id, status="all"):
    data = client.ozon_data.items.find_one({
        "creds": f"{api_key}:{client_id}"
    })
    if data is None:
        return None
    return data["ids"][status]


def get_postings_ids(api_key, client_id, status="all"):
    data = client.ozon_data.postings.find_one({
        "creds": f"{api_key}:{client_id}"
    })
    if data is None:
        return None
    return data["order_ids"][status]


def user_create(username, password):
    data = {
        'username': username,
        'password': password,
        "ozon_apikey": "",
        "client_id": ""
    }
    client.users.usernames.insert_one(data)
    data.pop("_id")
    data.pop("password")
    return True, data


def username_taken(username):
    return not (client.users.usernames.find_one({
        'username': username,
    }) is None)


def get_data(username):
    return not (client.users.user_data.find_one({
        'username': username
    }) is None)


def put_confirmation_token(username, password):
    token = secrets.token_urlsafe()
    client.users.confirmation_tokens.insert_one({
        'token': token,
        'username': username,
        'password': password
    })
    return token


def get_confirmation_token(token):
    data = client.users.confirmation_tokens.find_one({
        'token': token
    })
    if data is None:
        return False, 'Not found'
    username, password = data["username"], data["password"]
    client.users.confirmation_tokens.delete_one(data)

    return True, (username, password)
'''
def
db = client["Database0"]
collection = db["Collection0"]
inserted_id = collection.insert_one({
    "user_id": 2,
    "client_id": 836,
    "api_key": "y72g8e87q3us8f9es-dawdyduyegus"
}).inserted_id
print(db.list_collection_names())
pprint(collection.find_one())
pprint(collection.find_one({"_id": inserted_id}))'''