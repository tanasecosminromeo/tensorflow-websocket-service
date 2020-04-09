#!/bin/bash

needs_install () {
    [ ! -x "$(command -v $1)" ]
}

if needs_install docker; then
    echo "Please install docker";
    exit;
fi

if [ ! -f '.env' ]; then
    echo "Install default .env file - please check and amend if you want different ports"
    cp .env.dist .env
fi 

read_var() {
    MY_VAR=$(grep $1 .env | xargs)
    echo ${MY_VAR#*=}
}

exec () {
    docker exec -td --user $(id -u) $CONTAINER_NAME $1 $2 $3 $4 $5 $6
}

exec_wo () {
    docker exec -t $CONTAINER_NAME $1 $2 $3 $4 $5 $6
}

IMAGE=tanasecosminromeo/tensorflow-ws:latest
CONTAINER_NAME=tcr-tensorflow-ws

case "$1" in
'run'|'up')
    mkdir -p -m 777 var/logs
    mkdir -p -m 777 var/models

    HTTP_PORT=$(read_var HTTP_PORT)
    WEBSOCKET_PORT=$(read_var WEBSOCKET_PORT)
    MAX_MEMORY=$(read_var MAX_MEMORY)

    echo "Running $IMAGE as $CONTAINER_NAME exposing $HTTP_PORT as the HTTP port and $WEBSOCKET_PORT as the web socket port"


    ALREADY_RUNNING=$(docker ps -aqf "name=tcr-tensorflow-ws")

    if [ ! -z $ALREADY_RUNNING ]; then
        docker start $CONTAINER_NAME
    else
        docker run -d --name $CONTAINER_NAME -v ${PWD}:/code --env-file ./.env -p $HTTP_PORT:8000 -p $WEBSOCKET_PORT:8001 -m $MAX_MEMORY -u $(id -u ${USER}):$(id -g ${USER}) $IMAGE
    fi

    exec pkill -f python3
    exec python3 httpserver.py
    exec python3 websocket.py

    ##Todo: Remove this. It should be run by the socket WHEN required
    exec python3 src/detect ssd_mobilenet_v1_coco_11_06_2017 
;;
'exec')
    USER=$(whoami)
    echo "Entering container as $USER"
    docker exec -it $CONTAINER_NAME bash
;;
'sudo')
    echo "Entering container as root"
    docker exec -it --user root $CONTAINER_NAME bash
;;
'stop')
    echo "Stopping $CONTAINER_NAME"
    docker stop $CONTAINER_NAME
;;
'logs')
    echo "Logs of $CONTAINER_NAME"
    docker logs $CONTAINER_NAME
;;
'restart')
    echo "Restarting $CONTAINER_NAME"
    ./app stop
    ./app run
;;
'remove')
    echo "Removing $CONTAINER_NAME"
    docker stop $CONTAINER_NAME
    docker rm $CONTAINER_NAME
;;
'build')
	echo 'Building $IMAGE image'
    docker build -t $IMAGE .
;;
'socket')
	echo 'Refresh socket'
    
    exec pkill -f websocket.py
    exec python3 websocket.py
;;
'http')
	echo 'Refresh http'
    
    exec pkill -f httpserver.py
    exec python3 httpserver.py
;;
'detections')
	echo 'Refresh socket'
    
    exec pkill -f detect.py
;;
'ps')
    exec_wo ps au
;;
'kill')
    if [ -z "$2" ]; then
        echo "Which process do you want to kill?"
        exec_wo ps au
        read -p "Your command:" process
        ./app kill $process
        exit;
    fi
    exec_wo pkill -f $2
;;
*)
    echo -e '\n'
    echo 'Container commands:'
    echo -e '\t./app run\t\t - Starts the container'
    echo -e '\t./app exec\t\t - Enter container'
    echo -e '\t./app sudo\t\t - Enter container as root'
    echo -e '\t./app stop\t\t - Stops the container'
    echo -e '\t./app logs\t\t - Show all container logs'
    echo -e '\t./app restart\t\t - Re-creates the container'
    echo -e '\t./app remove\t\t - Removes the container'
    echo -e '\t./app build\t\t - Build image'

    echo -e '\n'
    echo 'Application commands:'
    echo -e '\t./app socket\t\t - Restarts the web socket server'
    echo -e '\t./app http\t\t - Restarts the http server'
    echo -e '\t./app detections\t - Kills any unset detect.py children'

    echo 'Other commands:'
    echo -e '\t./app ps\t\t - Shows all running processes'
    echo -e '\t./app kill\t\t - Kill specific process'

    echo -e '\n'
    read -p "Your command:" command
    ./app $command
;;
esac