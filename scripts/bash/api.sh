#!/bin/bash

docker run --rm --mount type=bind,source=.,destination=/ja_api nauseousspartan/ja_api $1
