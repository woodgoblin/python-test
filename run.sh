#!/bin/bash

case "$1" in
  start)
    poetry run dotenv -f .env run fastapi run
    ;;
  start-dev)
    poetry run dotenv -f .env run fastapi dev --reload
    ;;
  test)
    poetry run dotenv -f .env.test run pytest
    ;;
  *)
    echo "Usage: $0 {start|start-dev|test}"
    exit 1
esac
