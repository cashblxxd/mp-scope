# import pymongo
from pprint import pprint
import secrets
from mongo_queue.queue import Queue
import string
import random
import gridfs


def user_exist(username, password, client):
    data = client.users.usernames.find_one({
        'username': username,
        'password': password
    })
    if data is None:
        return (False,)
    data.pop("_id")
    data.pop("password")
    return True, data


def clear_queue(client):
    client.update_queue_db.update_queue.delete_many({})
    client.update_queue_db.job_ids.delete_many({})
    client.update_queue_db.sessions_active.delete_many({})


#clear_queue()


def get_session(uid, client):
    return client.sessions_data.sessions_active.find_one({
        "uid": uid
    })


def init_session(uid, client):
    client.sessions_data.sessions_active.delete_one({
        "uid": uid
    })
    client.sessions_data.sessions_active.insert_one({
        "uid": uid,
        "users": {},
        "order": [],
        "cur_pos": 1,
        "active": "dashboard",
        "tab": "items_all"
    })


def modify_session(uid, data, client):
    client.sessions_data.sessions_active.update_one({
        "uid": uid
    }, {"$set": data})


def delete_session(uid, client):
    client.sessions_data.sessions_active.delete_one({
        "uid": uid
    })


def mark_pending(job_id, client):
    client.update_queue_db.job_ids.insert_one({
        "job_id": job_id
    })


def mark_done(job_id, client):
    client.update_queue_db.job_ids.delete_one({
        "job_id": job_id
    })


def check_job(job_id, client):
    return client.update_queue_db.job_ids.find_one({
        "job_id": job_id
    }) is None


def get_items(api_key, client_id, client):
    return client.ozon_data.items.find_one({
        "creds": f"{api_key}:{client_id}"
    })


def get_postings(api_key, client_id, client):
    return client.ozon_data.postings.find_one({
        "creds": f"{api_key}:{client_id}"
    })


#mark_done("job1234")


def save_file(api_key, client_id, name, content, client):
    fs = gridfs.GridFS(client.files)
    file_id = fs.put(content, filename=name)
    data = client.user_files_list.user_files_list.find_one({
        "creds": f"{api_key}:{client_id}"
    })
    if data is None:
        data = {
            "creds": f"{api_key}:{client_id}",
            "data": {},
        }
    data["data"][name] = {
        "file_id": file_id
    }
    if "_id" in data:
        client.user_files_list.user_files_list.update_one({
            "_id": data["_id"]
        }, {"$set": data})
    else:
        client.user_files_list.user_files_list.insert_one(data)


def get_files_list(api_key, client_id, client):
    data = client.user_files_list.user_files_list.find_one({
        "creds": f"{api_key}:{client_id}"
    })
    if data is None:
        return {}
    return data["data"]


def get_file(f_id, client):
    fs = gridfs.GridFS(client.files)
    return fs.get(f_id).read()


def delete_file(api_key, client_id, filename, client):
    data = client.user_files_list.user_files_list.find_one({
        "creds": f"{api_key}:{client_id}"
    })
    if data is None:
        return
    pprint(data)
    delete_file_gridfs(data["data"][filename]["file_id"], client)
    data["data"].pop(filename, 0)
    client.user_files_list.user_files_list.update_one({
        "_id": data["_id"]
    }, {"$set": data})


def delete_file_gridfs(f_id, client):
    fs = gridfs.GridFS(client.files)
    fs.delete(f_id)


def insert_deliver_job(api_key, client_id, posting_numbers, job_id, client):
    queue = Queue(client.update_queue_db.update_queue, consumer_id=''.join(random.choice(string.ascii_lowercase) for i in range(10)), timeout=300, max_attempts=3)
    queue.put({"api_key": api_key, "client_id": client_id, "posting_numbers": posting_numbers,  "job_id": job_id}, channel="deliver_queue")
    mark_pending(job_id, client)


def insert_items_update_job(api_key, client_id, job_id, client):
    queue = Queue(client.update_queue_db.update_queue, consumer_id=''.join(random.choice(string.ascii_lowercase) for i in range(10)), timeout=300, max_attempts=3)
    queue.put({"api_key": api_key, "client_id": client_id, "job_id": job_id}, channel="items_priority")
    mark_pending(job_id, client)


def insert_items_regular_update(api_key, client_id, job_id, client):
    queue = Queue(client.update_queue_db.update_queue, consumer_id=''.join(random.choice(string.ascii_lowercase) for i in range(10)), timeout=300, max_attempts=3)
    queue.put({"api_key": api_key, "client_id": client_id, "job_id": job_id}, channel="items_queue")
    mark_pending(job_id, client)


def insert_postings_update_job(api_key, client_id, job_id, client):
    queue = Queue(client.update_queue_db.update_queue, consumer_id=''.join(random.choice(string.ascii_lowercase) for i in range(10)), timeout=300, max_attempts=3)
    queue.put({"api_key": api_key, "client_id": client_id, "job_id": job_id}, channel="postings_priority")
    mark_pending(job_id, client)
    print("INSERTED")


def insert_postings_regular_update(api_key, client_id, job_id, client):
    queue = Queue(client.update_queue_db.update_queue, consumer_id=''.join(random.choice(string.ascii_lowercase) for i in range(10)), timeout=300, max_attempts=3)
    queue.put({"api_key": api_key, "client_id": client_id, "job_id": job_id}, channel="postings_queue")
    mark_pending(job_id, client)


def insert_act_job(api_key, client_id, job_id, client):
    queue = Queue(client.update_queue_db.update_queue, consumer_id=''.join(random.choice(string.ascii_lowercase) for i in range(10)), timeout=300, max_attempts=3)
    queue.put({"api_key": api_key, "client_id": client_id, "job_id": job_id}, channel="act_queue")
    mark_pending(job_id, client)


def insert_labels_upload_job(api_key, client_id, posting_numbers, job_id, client):
    queue = Queue(client.update_queue_db.update_queue, consumer_id=''.join(random.choice(string.ascii_lowercase) for i in range(10)), timeout=300, max_attempts=3)
    queue.put({"api_key": api_key, "client_id": client_id, "job_id": job_id, "posting_numbers": posting_numbers}, channel="labels_queue")
    mark_pending(job_id, client)


def get_items_ids(api_key, client_id, client, status="all"):
    data = client.ozon_data.items.find_one({
        "creds": f"{api_key}:{client_id}"
    })
    if data is None:
        return None
    return data["ids"][status]


def get_postings_ids(api_key, client_id, client, status="all"):
    data = client.ozon_data.postings.find_one({
        "creds": f"{api_key}:{client_id}"
    })
    if data is None:
        return None
    return data["order_ids"][status]


def user_create(username, password, client):
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


def username_taken(username, client):
    return not (client.users.usernames.find_one({
        'username': username,
    }) is None)


def get_data(username, client):
    return not (client.users.user_data.find_one({
        'username': username
    }) is None)


def put_confirmation_token(username, password, client):
    token = secrets.token_urlsafe()
    client.users.confirmation_tokens.insert_one({
        'token': token,
        'username': username,
        'password': password
    })
    return token


def get_confirmation_token(token, client):
    data = client.users.confirmation_tokens.find_one({
        'token': token
    })
    if data is None:
        return False, 'Not found'
    username, password = data["username"], data["password"]
    client.users.confirmation_tokens.delete_one(data)
    return True, (username, password)
