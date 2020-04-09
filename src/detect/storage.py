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