# We use redis to store all of the info so it can be retrieved via web sockets
# We are making some custom functions as everything will be json encoded/decoded
import redis, json, logging
logger = logging.getLogger(__name__)

storage = redis.Redis()
class store:
    def set(name, value):
        storage.set(name, json.dumps(value))

    def get(name):
        return json.loads(storage.get(name))

    def llen(listName):
        return storage.llen(listName)

    def lpop(listName):
        return json.loads(storage.lpop(listName))

    def rpop(listName):
        return json.loads(storage.rpop(listName))

    def lpush(listName, data):
        return storage.lpush(listName, json.dumps(data))

    def rpush(listName, data):
        return storage.rpush(listName, json.dumps(data))