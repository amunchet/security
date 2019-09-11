#!/bin/bash

# TODO: Check to make sure the current user is part of the docker group, otherwise won't be able to write to the cameras directory from emulator

# Sudo will NOT work

env DATA_DIR=. USER_ID=1000 GROUP_ID=1000 docker-compose up #--build
