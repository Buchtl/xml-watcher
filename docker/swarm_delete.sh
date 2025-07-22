#!bin/bash
STACK_NAME=xml-watcher
docker stack rm $STACK_NAME
docker swarm leave --force
docker system prune
docker volume rm xml-watcher_xml-watcher
