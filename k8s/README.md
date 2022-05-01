
# init minikube
minikube start

minikube stop

# use docker in minikube
eval $(minikube docker-env)

docker build -f Dockerfile -t moudle_redis:test .

# Namespace

kubectl create ns redis

kubectl get ns

# Storage Class

kubectl get storageclass

# Deployment: Redis nodes

cd k8s
kubectl apply -n redis -f ./redis/redis-configmap.yaml
kubectl apply -n redis -f ./redis/redis-statefulset.yaml

kubectl -n redis get pods
kubectl -n redis get pv

kubectl -n redis logs redis-0
kubectl -n redis logs redis-1
kubectl -n redis logs redis-2

kubectl -n redis delete statefulset redis

kubectl -n redis logs redis-0 -c config

# Test replication status

kubectl -n redis exec -it redis-0 sh
redis-cli
auth a-very-complex-password-here
info replication

# Deployment: Redis Sentinel (3 instances)

cd k8s/
kubectl apply -n redis -f ./sentinel/sentinel-statefulset.yaml

kubectl -n redis get pods
kubectl -n redis get pv
kubectl -n redis logs sentinel-0

kubectl -n redis delete statefulset sentinel



kubectl -n redis delete pods redis-0


# Reference

- [redis:6.0-alpine Dockerfile](https://github.com/docker-library/redis/blob/84c36a0967bcfa8a9c39cb899464785c5f2cf5ef/6.0/alpine/Dockerfile#L99)

- [redislabs/redismod](https://hub.docker.com/r/redislabs/redismod/dockerfile)

- [Linux 的 shell script 中，遇到 unexpected operator 的解決方法](https://michael-hsu.medium.com/linux-%E7%9A%84-shell-script-%E4%B8%AD-%E9%81%87%E5%88%B0-unexpected-operator-%E7%9A%84%E8%A7%A3%E6%B1%BA%E6%96%B9%E6%B3%95-16c462d16c07)

- [[Linux] sh 和 bash 之間的差異](https://clay-atlas.com/blog/2020/07/08/linux-cn-note-sh-bash-dash-point/)