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
