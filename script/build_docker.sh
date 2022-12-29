#!/bin/bash

__dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source ${__dir}/build_base.sh

docker build -t hostyourdocs:local build_image