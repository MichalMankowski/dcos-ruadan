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
Library     libs/HealthLibrary.py

*** Variables ***
${DCOS_ADDRESS}    127.0.0.1

*** Keywords ***
Check services health
    [Arguments]   ${service_name}
    Get health report    ${DCOS_ADDRESS}
    Services should be healthly   ${service_name}

Check role health
    [Arguments]   ${role_name}
    Get health report    ${DCOS_ADDRESS}
    Role should be healthly   ${role_name}

*** Test cases ***
Masters should be healthly
    Check role health   master

Slaves should be healthly
    Check role health   agent

Public slaves should be healthly
    Check role health   agent_public

Diagnostics services should be healthly
    Check services health    Diagnostics

Diagnostics socket services should be healthly
    Check services health    Diagnostics socket

Admin Router Reloader services should be healthly
    Check services health    Admin Router Reloader

Admin Router Reloader Timer socket services should be healthly
    Check services health    Admin Router Reloader Timer

Admin Router Master services should be healthly
    Check services health    Admin Router Master

Admin Router Agent services should be healthly
    Check services health    Admin Router Agent

Erlang Port Mapping Daemon services should be healthly
    Check services health    Erlang Port Mapping Daemon

Generate resolv.conf services should be healthly
    Check services health    Generate resolv.conf

Generate resolv.conf Timer services should be healthly
    Check services health    Generate resolv.conf Timer

Logrotate Mesos Master services should be healthly
    Check services health    Logrotate Mesos Master

Logrotate Mesos Agent services should be healthly
    Check services health    Logrotate Mesos Agent

Logrotate Timer services should be healthly
    Check services health    Logrotate Timer

Mesos Master services should be healthly
    Check services health    Mesos Master

Mesos Agent services should be healthly
    Check services health    Mesos Agent

Mesos Agent Public services should be healthly
    Check services health    Mesos Agent Public

Layer 4 Load Balancer services should be healthly
    Check services health    Layer 4 Load Balancer

Navstar services should be healthly
    Check services health    Navstar

Pkgpanda API services should be healthly
    Check services health    Pkgpanda API

Pkgpanda API socket services should be healthly
    Check services health    Pkgpanda API socket

REX-Ray services should be healthly
    Check services health    REX-Ray

Signal services should be healthly
    Check services health    Signal

Signal Timer services should be healthly
    Check services health    Signal Timer

DNS Dispatcher Watchdog services should be healthly
    Check services health    DNS Dispatcher Watchdog

DNS Dispatcher Watchdog Timer services should be healthly
    Check services health    DNS Dispatcher Watchdog Timer

DNS Dispatcher services should be healthly
    Check services health    DNS Dispatcher

Package services services should be healthly
    Check services health    Package Service

Exhibitor services should be healthly
    Check services health    Exhibitor

Mesos History services should be healthly
    Check services health    Mesos History

Marathon services should be healthly
    Check services health    Marathon

Mesos DNS services should be healthly
    Check services health    Mesos DNS

OAuth services should be healthly
    Check services health    OAuth

Jobs services services should be healthly
    Check services health    Jobs Service
