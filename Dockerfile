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
