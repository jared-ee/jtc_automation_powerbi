#!/bin/bash

SELENIUM_IMAGE="selenium/standalone-chromium"
API_IMAGE="nauseousspartan/ja_api"

docker pull $SELENIUM_IMAGE
docker pull $API_IMAGE
