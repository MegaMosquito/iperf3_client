all: build run

build:
	docker build -t iperf3_client .

dev: build
	-docker rm -f iperf3_client 2> /dev/null || :
	docker run -it --name iperf3_client --net=host --volume `pwd`:/outside iperf3_client /bin/bash

run:
	-docker rm -f iperf3_client 2>/dev/null || :
	docker run -d --name iperf3_client --net=host --volume `pwd`:/outside iperf3_client

exec:
	docker exec -it iperf3_client /bin/sh

stop:
	-docker rm -f iperf3_client 2>/dev/null || :

clean: stop
	-docker rmi iperf3_client 2>/dev/null || :

.PHONY: all build dev run exec stop clean

