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
Library     libs/ExhibitorLibrary.py

*** Variables ***
${EXHIBITOR_ADDRESS}    127.0.0.1
${CLUSTER_SIZE}    3

*** Test cases ***
Exhibitor should be up and running
    Get Exhibitor cluster status    ${EXHIBITOR_ADDRESS}
    Status code should be    200

Exhibitor cluster should have expected size
    Get Exhibitor cluster status    ${EXHIBITOR_ADDRESS}
    Cluster size should be     ${CLUSTER_SIZE}

Exhibitor cluster should have leader elected
    Get Exhibitor cluster status    ${EXHIBITOR_ADDRESS}
    Leader should be elected

Exhibitor nodes should be serving
    Get Exhibitor cluster status    ${EXHIBITOR_ADDRESS}
    All nodes should be serving
