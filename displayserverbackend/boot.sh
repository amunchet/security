#!/bin/sh

. venv/bin/activate

export LC_ALL=en_US.utf-8
export LANG=en_US.utf-8

while true; do
  echo "DB URL = $DATABASE_URL"
  if flask db upgrade; then
    break
  fi
  echo Flask db upgrade command failed, retrying in 5 secs...
  sleep 5
done

# save db url in the file
echo "export DATABASE_URL=$DATABASE_URL" > /home/appuser/dbenv

crond && python displayserverbackend.py
