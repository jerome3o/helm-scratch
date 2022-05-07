# Helm chart scratch

In an attempt to learn a bit about how write helm charts I thought I'd go from 0 to service in a blank repo to solidify my understanding.

In this repo:
* `app/` an http api written in python using FastAPI that connects to a postgreSQL database.
* `db/` just contains a little bash script for setting up a postgres instance using docker 
* `k8s/` k8s object yaml definitions for running this service on a cluster with a postgres instance
* `chart/` a helm chart that reduces the boiler of the k8s files