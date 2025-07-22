
#!/bin/bash
IP=192.168.2.72
#$1
STACK_NAME=xml-watcher

docker swarm init --advertise-addr $IP
docker stack deploy -c <(docker-compose config) $STACK_NAME
docker stack ls
docker stack services $STACK_NAME
docker stack ps $STACK_NAME