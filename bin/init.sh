#!/usr/bin/env bash

add-apt-repository ppa:nginx/stable
apt-get update && sudo apt-get upgrade
apt-get install nginx
