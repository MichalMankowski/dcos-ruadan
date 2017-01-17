#!/bin/bash
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

robot --variable MARATHON_ADDRESS:$MARATHON_ADDRESS --variable EXHIBITOR_ADDRESS:$EXHIBITOR_ADDRESS --variable DCOS_ADDRESS:$DCOS_ADDRESS --variable CLUSTER_SIZE:$CLUSTER_SIZE /opt/dcos-sanity-tests/*.robot
cd /
cp report.html index.html
python -m SimpleHTTPServer
