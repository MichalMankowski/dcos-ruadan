# DCOS Sanity tests

## Manual verification

* Go to **http://master-ip-address:8181** and verify that:
	* All ZooKeepers are in **serving** status,
	* Circle near each server is green ;),
	* Amount of servers depends on your configuration - 1 for single master, 3+ for multi master configuration.
* Go to **http://master-ip-address:5050** and verify that:
	* All agents are activated,
	* There are no orphaned tasks.
* Go to **http://master-ip-address:8080** to verify that Marathon is up and running.
* Go to **http://master-ip-address**:
	* Verify that you are able to sign in,
	* Verify that DC/OS version in the bottom left corner is the correct version,
	* "Dashboard" tab:
		* Click on "View all 35 Components" button and make sure that all components are healthly,
	* "Nodes" tab:
		* Verify that amount of nodes corresponds to the amount of nodes that was requested,
		* Verify that all nodes are healthly.
* Check if it is possible to run Docker containers:
  * Go to "Services" tab,
  * Click on "Deploy service",
  * Type "docker-test" in ID field,
  * Assign resources to the container - 0.5 CPU, 256 MB RAM, 0 MB of disk, 1 instance,
  * Click on "Container Settings" tab,
  * Type "dockercloud/hello-world" in container image field,
  * Click on "Health Checks" tab,
  * Select TCP protocol,
  * Type 3 in grace period field,
  * Type 5 in interval field,
  * Type 5 in timeout field,
  * Type 3 in maximum consecutive failures field,
  * Select "Port number" from dropdown list,
  * Type 80 in port number field,
  * Go to "Services" tab,
  * Wait for your container to be in "Healthly" status

## Automated verification

```
docker build -t containerlabs:dcos-sanity-tests .
docker run -d -e EXHIBITOR_ADDRESS=192.168.1.2 -e MARATHON_ADDRESS=192.168.1.2 -e DCOS_ADDRESS=192.168.1.2 -e CLUSTER_SIZE=3 -p 8000:8000 --name dcos-sanity-tests containerlabs:dcos-sanity-tests
```
