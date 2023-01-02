#!/bin/bash

__dir_rel="$(dirname "${BASH_SOURCE[0]}")"

source "${__dir_rel}/build_base.sh"

docker build -t hostyourdocs:local build_image
