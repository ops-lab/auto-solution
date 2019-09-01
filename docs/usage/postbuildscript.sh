#!/bin/bash

ROOT_PATH=$(cd $(dirname $0); pwd -P)

BUILD_URL=$1
mode=${2:-product}

source ${ROOT_PATH}/venv/bin/activate
python ${ROOT_PATH}/venv/lib/python2.7/site-packages/auto_solution/solution.py --build_url "${BUILD_URL}" --mode "${mode}"
