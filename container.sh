#!/bin/bash

NAME="places_scraper_api"

if [[ $1 == "--build" || $1 == "-b" ]];then
    docker build . -t $NAME

elif [[ $1 == "--run" || $1 == "-r" ]];then
    xhost +
    docker run --rm -it \
        -v $(pwd):/app \
        -v /tmp/.X11-unix/:/tmp/.X11-unix \
        -p 8080:8080 \
        -e DISPLAY=$DISPLAY \
        --shm-size="2g" \
        --name $NAME \
        --hostname $NAME \
        $NAME bash

elif [[ $1 == "--attach" || $1 == "-a" ]];then
    docker exec -it $NAME bash
fi