import os

import redis
from rq import Worker, Queue, Connection

listen = ['high', 'default', 'low']

redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')

conn = redis.from_url(redis_url)

if __name__ == '__main__':
  print("worker test 1")
  with Connection(conn):
    print("worker test 2")
    worker = Worker(map(Queue, listen))
    print("worker test 3")
    worker.work()
    print("worker test 4")
