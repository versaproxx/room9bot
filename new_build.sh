#/bin/bash

echo "Trying pull repository"
git pull
echo "Git repository pulled"

echo "Stoping all bot containers"
docker stop $(docker ps -aq)
echo "All containers stoped"

echo "Deleting old container versions"
docker rm $(docker ps -aq)
echo "Deleted"

echo "Delete all images of bot"
docker rmi $(docker images -q)
echo "Images deleted"

echo "Starting build new bot version"
docker build -t 9bot .
echo "New version of bot builded with name 9bot"

echo "Starting new container"
docker run -d -v /opt/bot_files:/opt/9bot/bot_files -d 9bot
echo "Check your new version of bot in chat"
