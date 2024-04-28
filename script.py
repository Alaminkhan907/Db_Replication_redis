import redis
import time
master = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

master.mset({'name': 'Alamin', 'age': '27', 'sex': 'male'})

time.sleep(2)
slave1 = redis.StrictRedis(host='localhost', port=6380, decode_responses=True)
slave2 = redis.StrictRedis(host='localhost', port=6381, decode_responses=True)

# Get the values of the keys from each slave
value1 = slave1.mget('name', 'age', 'sex')
print("Values from slave 1:", value1)

value2 = slave1.mget('name', 'age', 'sex')
print("Values from slave 1:", value2)
