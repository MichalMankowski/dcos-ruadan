import requests


class ExhibitorLibrary(object):
    def __init__(self):
        self._status_code = ''
        self._cluster = ''

    def get_exhibitor_cluster_status(self, exhibitor_address):
        response = requests.get(
            'http://{}:8181/exhibitor/v1/cluster/status'.format(
                exhibitor_address))
        self._status_code = str(response.status_code)
        try:
            self._cluster = response.json()
        except ValueError:
            pass

    def status_code_should_be(self, expected_status):
        if expected_status != self._status_code:
            raise AssertionError(
                'Expected status to be {}, received {}.'.format(
                    expected_status, self._status_code))

    def cluster_size_should_be(self, cluster_size):
        actual_cluster_size = str(len(self._cluster))
        if cluster_size != actual_cluster_size:
            raise AssertionError(
                'Expected cluster size to be {}, received {}.'.format(
                    cluster_size, actual_cluster_size))

    def leader_should_be_elected(self):
        leaders = sum(item['isLeader'] for item in self._cluster)
        if leaders != 1:
            raise AssertionError('Expected single leader, got {}.'.format(
                leaders))

    def all_nodes_should_be_serving(self):
        if not all(item['description'] == 'serving' for item in self._cluster):
            raise AssertionError('Expected all nodes to be serving.')
