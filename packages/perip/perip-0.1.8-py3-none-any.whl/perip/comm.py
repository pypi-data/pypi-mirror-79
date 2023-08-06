import redis

class Comm:
    def __init__(self, host, port, password):
        self._redis = redis.Redis(host=host,
                        port=port,
                        password=password)

            # return redis.Redis(host='ec2-75-101-199-232.compute-1.amazonaws.com',
            #                    port=7599,
            #                    password='p525f81fc5bf9a369922112084c158114e3978bc3042d9a76172a8508c7cd26ce')

    def set_key(self, k, v):
        self._redis.set(k, v)



    # def myfunc(self):
    #     print("Hello my name is " + self.name)