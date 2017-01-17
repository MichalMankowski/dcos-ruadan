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