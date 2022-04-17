import os

import redis
from fastapi import FastAPI
from redis import Sentinel

app = FastAPI()

@app.get("/")
async def root():
    sentinel = Sentinel(
        [("sentinel-0", 5000), ("sentinel-1", 5000), ("sentinel-2", 5000)],
        socket_timeout=0.5
    )

    master = sentinel.master_for(
        'mymaster', socket_timeout=0.5, password=os.environ.get("REDIS_PWD")
    )

    count = master.get("count")
    if count is None:
        count = 1

    master.set('count', int(count) + 1)
    return {'message':"current count : " + str(int(count) + 1)}
