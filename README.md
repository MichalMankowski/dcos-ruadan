# Ruadan

Ruadan is a set of automated DC/OS sanity tests.

![Test report](images/main.png)

## Getting started

Simply fetch the Docker container for Ruadan:

```
docker pull kamsz/ruadan
```

And run it:

```
docker run -d -e EXHIBITOR_ADDRESS=192.168.1.2 -e MARATHON_ADDRESS=192.168.1.2 -e DCOS_ADDRESS=192.168.1.2 -e CLUSTER_SIZE=3 -p 8000:8000 --name ruadan kamsz/ruadan
```

Test report will be available at http://localhost:8000.

## Docker environment variables

* `EXHIBITOR_ADDRESS` - Hostname or IP address of the Exhibitor instance (or load balancer).
* `MARATHON_ADDRESS` - Hostname or IP address of the Marathon instance (or load balancer).
* `DCOS_ADDRESS` - Hostname or IP address of the DC/OS instance (or load balancer).
* `CLUSTER_SIZE` - Size of the Mesos cluster.

## Example Marathon service definition

```
{
  "id": "ruadan",
  "cmd": null,
  "cpus": 0.5,
  "mem": 128,
  "disk": 0,
  "instances": 1,
  "executor": null,
  "fetch": null,
  "constraints": null,
  "acceptedResourceRoles": null,
  "user": null,
  "container": {
    "docker": {
      "image": "kamsz/ruadan",
      "forcePullImage": false,
      "privileged": false,
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp",
          "name": "ruadan",
          "servicePort": 8000,
          "labels": {
            "VIP_0": "ruadan:8000"
          },
          "hostPort": 0
        }
      ],
      "network": "USER"
    }
  },
  "labels": null,
  "healthChecks": [
    {
      "protocol": "TCP",
      "port": 8000
    }
  ],
  "env": {
    "EXHIBITOR_ADDRESS": "192.168.1.2",
    "MARATHON_ADDRESS": "192.168.1.2",
    "DCOS_ADDRESS": "192.168.1.2",
    "CLUSTER_SIZE": "3"
  },
  "ipAddress": {
    "networkName": "dcos"
  }
}
```

## More images!

### Detailed test report

![Detailed test report](images/detailed.png)

### Test log

![Test log](images/log.png)

## License

Ruadan is Open Source software released under the [Apache 2.0](LICENSE) license.
