#!/usr/bin/env bash

HOST="192.168.81.123"
PORT=21324
MESSAGE="\x02\x02\xff\x00\x00\x00\xff\x00\x00\x00\xff"

echo -en "$MESSAGE" > /dev/udp/$HOST/$PORT