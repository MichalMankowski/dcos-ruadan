#!/bin/bash
robot --variable MARATHON_ADDRESS:$MARATHON_ADDRESS --variable EXHIBITOR_ADDRESS:$EXHIBITOR_ADDRESS --variable DCOS_ADDRESS:$DCOS_ADDRESS --variable CLUSTER_SIZE:$CLUSTER_SIZE /opt/dcos-sanity-tests/*.robot
cd /
cp report.html index.html
python -m SimpleHTTPServer
