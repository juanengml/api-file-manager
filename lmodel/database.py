import redis
import json


class Formater(object):
    @staticmethod
    def format(item):
        if item:
            config = json.loads(item)
        else:
            config = "Device not found"
        return config

    @staticmethod
    def dumps(log_data):
        return json.dumps(log_data)


class Database(object):
    def __init__(self, host="192.168.0.48", port=6379, db=0):
        self.redis_conn = redis.StrictRedis(host=host, port=port, db=db)

    def select(self, id_device):
        config_json = self.redis_conn.get(id_device)
        config = Formater().format(config_json)
        return config

    def insert(self, id_device, log_data):
        log_data_dumps = Formater().dumps(log_data)
        self.redis_conn.set(id_device, log_data_dumps)
