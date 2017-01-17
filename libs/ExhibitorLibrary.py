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


class ExhibitorLibrary(object):
    """Library that handles Exhibitor test methods."""

    def __init__(self):
        """Class constructor."""

        self._status_code = ''
        self._cluster = ''

    def get_exhibitor_cluster_status(self, exhibitor_address):
        """Get Exhibitor cluster status.

        Args:
            exhibitor_address (str): Hostname or IP address of Exhibitor.
        Raises:
            AssertionError: When connection to Exhibitor failed.
        """

        url = 'http://{address}:8181/exhibitor/v1/cluster/status'.format(
            address=exhibitor_address)

        try:
            response = requests.get(url, timeout=30)
        except requests.exceptions.ConnectTimeout:
            raise AssertionError(
                'Timed out while trying to connect to {url}'.format(
                    url=url))
        except requests.exceptions.ConnectionError:
            raise AssertionError('Could not connect to {url}'.format(
                url=url))

        self._status_code = str(response.status_code)
        self._cluster = response.json()

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
                'Expected status to be {expected_status}, '
                'received {received_status}.'.format(
                    expected_status=expected_status,
                    received_status=self._status_code))

    def cluster_size_should_be(self, cluster_size):
        """Compare expected cluster size with actual cluster size.

        Args:
            cluster_size (str): Size of the cluster.

        Raises:
            AssertionError: When expected cluster size differs from the
            actual cluster size.
        """

        actual_cluster_size = str(len(self._cluster))
        if cluster_size != actual_cluster_size:
            raise AssertionError(
                'Expected cluster size to be {expected_size}, '
                'received {actual_size}.'.format(
                    expected_size=cluster_size,
                    actual_size=actual_cluster_size))

    def leader_should_be_elected(self):
        """Verify that leader is elected.

        Raises:
            AssertionError: When there is no leader or more than one leader.
        """

        leaders = sum(item['isLeader'] for item in self._cluster)
        if leaders != 1:
            raise AssertionError('Expected single leader, '
                                 'got {leader_count}.'.format(
                                     leader_count=leaders))

    def all_nodes_should_be_serving(self):
        """Verify that all nodes are serving.

        Raises:
            AssertionError: When not all nodes are serving.
        """

        if not all(item['description'] == 'serving' for item in self._cluster):
            raise AssertionError('Expected all nodes to be serving.')
