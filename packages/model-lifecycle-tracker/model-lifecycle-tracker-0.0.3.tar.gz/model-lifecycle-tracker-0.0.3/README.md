# model-tracker

A simple data store keeping track of models and things


### Running locally

* Get postgres up and running for local development

```
 docker pull postgres
 docker run --rm   --name pg-docker -e POSTGRES_PASSWORD=docker -d -p 5432:5432
```

* Flash database for quick dev

```
PGPASSWORD='docker' psql -h localhost -U postgres -c "drop database modeltracker" 
  && PGPASSWORD='docker' psql -h localhost -U postgres -c "create database modeltracker"
```

* Populate the basic type tables

```
python -m modeltracker.main
```

* Suppose you have been developing and wish to destroy all table contents:

```bash
python -m modeltracker.main -r
```

# Database dict
## To keep track of what is being produced by the modeltracker

**datastore_type** : Describes the datastore types, BQ or GCS for instance.

**feature_store_metrics** : Describes the metrics relating to each model in the model_catalog_id

**job** : Describes tasks that have been run

**model_catalog** : describes models and links to state_id

**model_output** : describes location and datastore type of model_output

**state** : Catalogue of states

**task_type** : Tracks tasks that occurr
