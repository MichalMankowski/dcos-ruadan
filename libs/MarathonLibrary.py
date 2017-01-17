import json
from time import sleep

import requests


class MarathonLibrary(object):
    def __init__(self):
        self._status_code = ''
        self._marathon = ''

    def get_marathon_status(self, marathon_address):
        response = requests.get('http://{}:8080/v2/info'.format(
            marathon_address))
        self._status_code = str(response.status_code)
        try:
            self._marathon = response.json()
        except ValueError:
            pass

    def status_code_should_be(self, expected_status):
        if expected_status != self._status_code:
            raise AssertionError(
                'Expected status to be {}, received {}.'.format(
                    expected_status, self._status_code))

    def leader_should_be_elected(self):
        if not self._marathon['elected']:
            raise AssertionError('Expected leader to be elected.')

    def verify_high_availability(self, cluster_size):
        cluster_size = int(cluster_size)

        if cluster_size > 1 and not self._marathon['marathon_config']['ha']:
            raise AssertionError('Expected high availability to '
                                 'be enabled for cluster size {}.'.format(
                                     cluster_size))

    def run_docker_container(self, marathon_address, docker_image):
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
        response = requests.post('http://{}:8080/v2/apps'.format(
            marathon_address), data=json.dumps(application),
                                 headers={'content-type': 'application/json'})
        if response.status_code != 201:
            raise AssertionError(
                'Expected status code to be 200, received {}'.format(
                    response.status_code))

        counter = 0
        while True:
            response = requests.get(
                'http://{}:8080/v2/apps/docker-test'.format(marathon_address))
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
        response = requests.delete('http://{}:8080/v2/apps/{}'.format(
            marathon_address, 'docker-test'))

        if response.status_code != 200:
            raise AssertionError(
                'Expected status code to be 200, received {}'.format(
                    response.status_code))
