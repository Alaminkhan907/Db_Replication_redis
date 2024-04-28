#start docker
docker compose up

#check data on docker

#master node
docker exec -it db-redis-master-1 redis-cli
mget name age sex
exit

#slave node
docker exec -it db-redis-slave1-1 redis-cli

# Once connected, use the following command to retrieve the values of the keys:

mget name age sex

docker exec -it db-redis-slave2-1 redis-cli

mget name age sex

#NOW Lets down master node and check if data avaiable or not

docker stop db-redis-master-1

docker exec -it db-redis-slave2-1 redis-cli

mget name age sex

#Now try to write data when master node is down

#Setting up Redis Sentinel with Docker:
docker network create redis-network
docker run -d --name redis-master --network redis-network redis:latest redis-server --port 6379
docker run -d --name redis-replica1 --network redis-network redis:latest redis-server --port 6379 --slaveof redis-master 6379
docker run -d --name redis-sentinel1 --network redis-network redis:latest redis-sentinel --port 26379 --sentinel announce-ip 127.0.0.1 --sentinel announce-port 26379 --sentinel monitor mymaster redis-master 6379 2

Setting up Redis Cluster with Docker:
docker network create redis-network
docker run -d --name redis-node1 --network redis-network redis:latest redis-server --port 7000 --cluster-enabled yes --cluster-config-file nodes.conf --cluster-node-timeout 5000 --appendonly yes
docker run -d --name redis-node2 --network redis-network redis:latest redis-server --port 7001 --cluster-enabled yes --cluster-config-file nodes.conf --cluster-node-timeout 5000 --appendonly yes

docker exec -it redis-node1 redis-cli --cluster create 127.0.0.1:7000 127.0.0.1:7001
# Db_Replication_redis
# Db_Replication_redis
