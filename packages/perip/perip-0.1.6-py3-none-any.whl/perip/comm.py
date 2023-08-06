import redis

def connect():
    return redis.Redis(host='ec2-75-101-199-232.compute-1.amazonaws.com', port=7599, password='p525f81fc5bf9a369922112084c158114e3978bc3042d9a76172a8508c7cd26ce')