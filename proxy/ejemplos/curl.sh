#!/bin/bash

proxy=$(curl --silent --proxy http://172.28.0.2:8888 'https://api.ipify.org?format.json')
no_proxy=$(curl --silent 'https://api.ipify.org?format.json')

cat << EOF
No proxy $no_proxy
Proxy $proxy
EOF
