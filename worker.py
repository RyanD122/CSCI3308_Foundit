import os

import redis
from rq import Worker, Queue, Connection

import praw
import nltk
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
from datetime import datetime, timedelta
import time
import os
from collections import Counter


listen = ['high', 'default', 'low']

redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')

conn = redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()

