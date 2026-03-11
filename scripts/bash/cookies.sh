#!/bin/bash

docker stop chromium

set -e

SELENIUM_IMAGE="selenium/standalone-chromium"

docker run --rm --name chromium -d -p 4444:4444 -p 7900:7900 --shm-size="2g" $SELENIUM_IMAGE

echo "Waiting for Selenium server to be ready..."

URL="http://localhost:4444/status"
until curl -s "$URL" | grep -q '"ready":[ ]*true'; do
	sleep 1
	echo "loading..."
done

echo "Selenium server is ready! Please visit it at http://localhost:7900/?autoconnect=1&resize=scale&password=secret"

docker run --rm --mount type=bind,source=.,destination=/ja_api nauseousspartan/ja_api sign_in auth

docker stop chromium
