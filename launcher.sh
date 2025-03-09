#!/bin/bash
if [[ $1 == "build" ]]; then
	echo "Building images..."
	docker buildx build -t lifprojet_api -f ./backend/Dockerfile.dev backend/
elif [[ $1 == "up" ]]; then
	echo "Launching containers..."
	docker compose -f compose.dev.yml up -d --build
elif [[ $1 == "down" ]]; then
	echo "Stopping containers..."
	docker compose -f compose.dev.yml down
else
	echo "Command not found, only available: build | up | down"
fi
