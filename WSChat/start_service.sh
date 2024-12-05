#!/usr/bin/env bash
##
## Starts service w/o docker (in virtual environment or directly in system)
##


## set flag of for dev-environment:
export ENVTYPE="DEV"

## start service:
echo "Start application:"
uvicorn app.main:app --reload --host 0.0.0.0 --port 5050 --proxy-headers
