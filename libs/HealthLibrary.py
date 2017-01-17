import requests


class HealthLibrary(object):
    def __init__(self):
        self._report = ''

    def get_health_report(self, dcos_address):
        response = requests.get('http://{}/system/health/v1/report'.format(
            dcos_address))

        if response.status_code != 200:
            raise AssertionError(
                'Expected status code to be 200, received {}.'.format(
                    response.status_code))
        self._report = response.json()

    def role_should_be_healthly(self, role):
        nodes = [values for _, values in self._report['Nodes'].iteritems()
                 if values['Role'] == role]

        if not all(item['Health'] == 0 for item in nodes):
            raise AssertionError(
                'Expected all nodes with role {} to be healthly.'.format(role))

    def services_should_be_healthly(self, service):
        all_services = [values['Units'] for _, values
                        in self._report['Nodes'].iteritems()]
        all_services = sum(all_services, [])
        filtered_services = [item for item in all_services
                             if item['PrettyName'] == service]

        if len(filtered_services) == 0:
            raise AssertionError('Could not find service {}'.format(service))

        if not all(item['Health'] == 0 for item in filtered_services):
            raise AssertionError(
                'Expected service {} to be healthly on all nodes.'.format(
                    service))
