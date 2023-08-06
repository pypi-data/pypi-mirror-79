import redis

class Comm:
    def __init__(self, host, port, password):
        self._redis = redis.Redis(host=host,
                        port=port,
                        password=password)

    def set_key(self, k, v):
        self._redis.set(k, v)

    def get_value_by_key(self, k):
        return self._redis.get(k)



    # def myfunc(self):
    #     print("Hello my name is " + self.name)