#!/bin/bash

set -e

docker build -t nauseousspartan/ja_api --platform linux/amd64,linux/arm64 .
