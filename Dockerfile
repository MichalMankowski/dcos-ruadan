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

FROM ubuntu:xenial
MAINTAINER Kamil Szczygiel <kszczygiel@container-labs.com>

ENV MARATHON_ADDRESS=127.0.0.1
ENV EXHIBITOR_ADDRESS=127.0.0.1
ENV DCOS_ADDRESS=127.0.0.1
ENV CLUSTER_SIZE=3

RUN apt-get update
RUN apt-get install -y python-pip
RUN pip install robotframework requests
RUN mkdir /opt/dcos-sanity-tests

COPY libs /opt/dcos-sanity-tests/libs
COPY *.robot /opt/dcos-sanity-tests/
COPY entrypoint.sh /opt/dcos-sanity-tests/entrypoint.sh

EXPOSE 8000
ENTRYPOINT /opt/dcos-sanity-tests/entrypoint.sh
