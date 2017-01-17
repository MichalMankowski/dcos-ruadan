# Copyright (c) 2017 Container Labs
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

*** Settings ***
Library     libs/MarathonLibrary.py

*** Variables ***
${MARATHON_ADDRESS}    127.0.0.1
${CLUSTER_SIZE}    3

*** Test cases ***
Marathon should be up and running
    Get Marathon status    ${MARATHON_ADDRESS}
    Status code should be    200

Marathon leader should be elected
    Get Marathon status    ${MARATHON_ADDRESS}
    Leader should be elected

Verify high availability
    Get Marathon status    ${MARATHON_ADDRESS}
    Verify high availability   ${CLUSTER_SIZE}

Verify that Docker is working
    Get Marathon status    ${MARATHON_ADDRESS}
    Run Docker container    ${MARATHON_ADDRESS}   dockercloud/hello-world
