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

import json
from time import sleep

import requests


class MarathonLibrary(object):
    """Library that handles Marathon test methods."""

    def __init__(self):
        """Class constructor."""

        self._status_code = ''
        self._marathon = ''

    def get_marathon_status(self, marathon_address):
        """Retrieve Marathon status information.

        Args:
            marathon_address (string): Hostname or IP address of Marathon.

        Raises:
            AssertionError: When connection to Marathon failed.
        """

        url = 'http://{marathon_address}:8080/v2/info'.format(
            marathon_address=marathon_address)

        try:
            response = requests.get(url, timeout=30)
        except requests.exceptions.ConnectTimeout:
            raise AssertionError(
                'Timed out while trying to connect to {url}'.format(url=url))
        except requests.exceptions.ConnectionError:
            raise AssertionError('Could not connect to {url}'.format(url=url))

        self._status_code = str(response.status_code)
        self._marathon = response.json()

    def status_code_should_be(self, expected_status):
        """Compare expected status code with actual status code.

        Args:
            expected_status (str): Expected status code.

        Raises:
            AssertionError: When expected status differs from the actual
            status code.
        """

        if expected_status != self._status_code:
            raise AssertionError(
                'Expected status to be {}, received {}.'.format(
                    expected_status, self._status_code))

    def leader_should_be_elected(self):
        """Verify that leader is elected.

        Raises:
            AssertionError: When leader is not elected.
        """

        if not self._marathon['elected']:
            raise AssertionError('Expected leader to be elected.')

    def verify_high_availability(self, cluster_size):
        """Verify that high availability is enabled on the cluster.

        Args:
            cluster_size (str): Size of the cluster.

        Raises:
            AssertionError: When high availability is not enabled.
        """

        cluster_size = int(cluster_size)

        if cluster_size > 1 and not self._marathon['marathon_config']['ha']:
            raise AssertionError('Expected high availability to '
                                 'be enabled for cluster '
                                 'size {cluster_size}.'.format(
                                     cluster_size=cluster_size))

    def run_docker_container(self, marathon_address, docker_image):
        """Test if it is possible to deploy Docker container.

        Args:
            marathon_address (string): Hostname or IP address of Marathon.
            docker_image (string): Name of Docker image to use.

        Raises:
            AssertionError: When connection to Marathon failed or
            Marathon was unable to create a container or
            timed out while waiting for a container to get healthly.
        """

        application = {
            'id': 'docker-test',
            'cpus': 0.5,
            'mem': 256,
            'disk': 0,
            'instances': 1,
            'env': {},
            'labels': {},
            'healthChecks': [
                {
                    'protocol': 'TCP',
                    'gracePeriodSeconds': 3,
                    'intervalSeconds': 5,
                    'port': 80,
                    'timeoutSeconds': 5,
                    'maxConsecutiveFailures': 3
                }
            ],
            'container': {
                'docker': {
                    'image': docker_image,
                    'network': 'HOST'
                },
                'type': 'DOCKER',
                'volumes': []
            }
        }

        create_url = 'http://{address}:8080/v2/apps'.format(
            address=marathon_address)

        try:
            response = requests.post(create_url, data=json.dumps(application),
                                     headers={
                                         'content-type': 'application/json'},
                                     timeout=30)
        except requests.exceptions.ConnectTimeout:
            raise AssertionError(
                'Timed out while trying to connect to {url}'.format(
                    url=create_url))
        except requests.exceptions.ConnectionError:
            raise AssertionError('Could not connect to {url}'.format(
                url=create_url))

        if response.status_code != 201:
            raise AssertionError(
                'Expected status code to be 201, '
                'received {status_code}'.format(
                    status_code=response.status_code))

        counter = 0
        while True:
            app_url = 'http://{address}:8080/v2/apps/docker-test'.format(
                address=marathon_address)

            try:
                response = requests.get(app_url, timeout=30)
            except requests.exceptions.ConnectTimeout:
                raise AssertionError(
                    'Timed out while trying to connect to {url}'.format(
                        url=app_url))
            except requests.exceptions.ConnectionError:
                raise AssertionError('Could not connect to {url}'.format(
                    url=app_url))

            data = response.json()
            if data['app']['tasksHealthy'] == 1:
                break

            if counter > 60:
                self._remove_docker_container(marathon_address)
                raise AssertionError('Timed out while waiting for container '
                                     'to get healthly.')
            counter += 1
            sleep(5)

        self._remove_docker_container(marathon_address)

    def _remove_docker_container(self, marathon_address):
        """Delete Docker container.

        Args:
            marathon_address (string): Hostname or IP address of Marathon.

        Raises:
            AssertionError: When connection to Marathon failed or
            Marathon was unable to delete a container.
        """

        delete_url = 'http://{address}:8080/v2/apps/{app}'.format(
            address=marathon_address, app='docker-test')

        try:
            response = requests.delete(delete_url, timeout=30)
        except requests.exceptions.ConnectTimeout:
            raise AssertionError(
                'Timed out while trying to connect to {url}'.format(
                    url=delete_url))
        except requests.exceptions.ConnectionError:
            raise AssertionError('Could not connect to {url}'.format(
                url=delete_url))

        if response.status_code != 200:
            raise AssertionError(
                'Expected status code to be 200, received {}'.format(
                    response.status_code))
