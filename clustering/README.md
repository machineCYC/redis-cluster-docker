# redis-cluster-docker

This proejct will build an api server to test the redis cluster with master redis failed

## Replication

Documentation [here](https://redis.io/topics/replication)

### Configuration

```
#persistence
dir /data
dbfilename dump.rdb
appendonly yes
appendfilename "appendonly.aof"

```
### redis-0 Configuration

```
protected-mode no
port 6379

#authentication
masterauth a-very-complex-password-here
requirepass a-very-complex-password-here
```
### redis-1 Configuration

```
protected-mode no
port 6379
slaveof redis-0 6379

#authentication
masterauth a-very-complex-password-here
requirepass a-very-complex-password-here

```
### redis-2 Configuration

```
protected-mode no
port 6379
slaveof redis-0 6379

#authentication
masterauth a-very-complex-password-here
requirepass a-very-complex-password-here

```

```

# remember to update above in configs!

docker network create redis

cd clustering/

#redis-0
docker run -d --rm --name redis-0 \
    --net redis \
    -v ${PWD}/redis-0:/etc/redis/ \
    redis:6.0-alpine redis-server /etc/redis/redis.conf

#redis-1
docker run -d --rm --name redis-1 \
    --net redis \
    -v ${PWD}/redis-1:/etc/redis/ \
    redis:6.0-alpine redis-server /etc/redis/redis.conf


#redis-2
docker run -d --rm --name redis-2 \
    --net redis \
    -v ${PWD}/redis-2:/etc/redis/ \
    redis:6.0-alpine redis-server /etc/redis/redis.conf

```

## Example Application

Run example application in video, to show application writing to the master

```
cd applications/
docker build -t fast_api:v1 .

docker run -it --rm --name fast_api \
--net redis \
-e REDIS_PWD="12345" \
-p 5000:5000 \
fast_api:v1

```

## Test Replication

Technically written data should now be on the replicas

```
# go to one of the clients
docker exec -it redis-2 sh
redis-cli
auth "a-very-complex-password-here"
keys *

```

## Running Sentinels

Documentation [here](https://redis.io/topics/sentinel)

```
#********BASIC CONFIG************************************
port 5000
sentinel monitor mymaster redis-0 6379 2
sentinel down-after-milliseconds mymaster 5000
sentinel failover-timeout mymaster 60000
sentinel parallel-syncs mymaster 1
sentinel auth-pass mymaster a-very-complex-password-here
#********************************************

```
Starting Redis in sentinel mode

```
cd clustering/

docker run -d --rm --name sentinel-0 --net redis \
    -v ${PWD}/sentinel-0:/etc/redis/ \
    redis:6.0-alpine \
    redis-sentinel /etc/redis/sentinel.conf

docker run -d --rm --name sentinel-1 --net redis \
    -v ${PWD}/sentinel-1:/etc/redis/ \
    redis:6.0-alpine \
    redis-sentinel /etc/redis/sentinel.conf

docker run -d --rm --name sentinel-2 --net redis \
    -v ${PWD}/sentinel-2:/etc/redis/ \
    redis:6.0-alpine \
    redis-sentinel /etc/redis/sentinel.conf


docker logs sentinel-0
docker exec -it sentinel-0 sh
redis-cli -p 5000
info
sentinel master mymaster

# clean up

docker rm -f redis-0 redis-1 redis-2
docker rm -f sentinel-0 sentinel-1 sentinel-2


```


## Reference

- [Redis on Kubernetes for beginners](https://www.youtube.com/watch?v=JmCn7k0PlV4&list=RDCMUCFe9-V_rN9nLqVNiI8Yof3w&start_radio=1&ab_channel=ThatDevOpsGuy)