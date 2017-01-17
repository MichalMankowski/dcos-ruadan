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

import requests


class HealthLibrary(object):
    """Library that handles Health test methods."""

    def __init__(self):
        """Class constructor."""

        self._report = ''

    def get_health_report(self, dcos_address):
        """Retrieve health report

        Args:
            dcos_address (str): Hostname or IP address of DC/OS.

        Raises:
            AssertionError: When connection to DC/OS failed or
            status code was not 200.
        """

        url = 'http://{address}/system/health/v1/report'.format(
            address=dcos_address)

        try:
            response = requests.get(url, timeout=30)
        except requests.exceptions.ConnectTimeout:
            raise AssertionError(
                'Timed out while trying to connect to {url}'.format(
                    url=url))
        except requests.exceptions.ConnectionError:
            raise AssertionError('Could not connect to {url}'.format(
                url=url))

        if response.status_code != 200:
            raise AssertionError(
                'Expected status code to be 200, '
                'received {status_code}.'.format(
                    status_code=response.status_code))
        self._report = response.json()

    def role_should_be_healthly(self, role):
        """Verify that specified is in healthly state.

        Args:
            role (str): Role name.

        Raises:
            AssertionError: When role is not found or
            role is not in healthly state.
        """

        nodes = [values for _, values in self._report['Nodes'].iteritems()
                 if values['Role'] == role]

        if len(nodes) == 0:
            raise AssertionError('Could not find role {role_name}'.format(
                role_name=role))

        if not all(item['Health'] == 0 for item in nodes):
            raise AssertionError(
                'Expected all nodes with role {role_name} '
                'to be healthly.'.format(role_name=role))

    def services_should_be_healthly(self, service):
        """Verify that specified service is in healthly state.

        Args:
            service (str): Service name.

        Raises:
            AssertionError: When service is not found or
            service is not in healthly state.
        """

        all_services = [values['Units'] for _, values
                        in self._report['Nodes'].iteritems()]
        all_services = sum(all_services, [])
        filtered_services = [item for item in all_services
                             if item['PrettyName'] == service]

        if len(filtered_services) == 0:
            raise AssertionError('Could not find '
                                 'service {service_name}'.format(
                                    service_name=service))

        if not all(item['Health'] == 0 for item in filtered_services):
            raise AssertionError(
                'Expected service {service_name} to '
                'be healthly on all nodes.'.format(service_name=service))
