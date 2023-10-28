# sms_simulation_project
### How to run

The project is set in a docker-containerized environment and can be easily launched using the command:

`docker-compose up` 

All the configurations are present in `app-config.yml`

It will automatically download all the base images and will launch the necessary services. A Docker daemon has to be running for it. 
Download the Docker Desktop from here:
https://www.docker.com/products/docker-desktop/
Please see here for more details - https://docs.docker.com/compose/ 

Respective launched applications can be found at

•	Kafka - <localhost:9092> (Inside containers it will be accessible as <kafka:29092>)

•	Logstash - http://localhost:5959/ 

•	Elasticsearch - http://localhost:9200/ 

•	Kibana - http://localhost:5601/ (Please import [‘export.ndjson’] file in Kibana to import dashboard analysis.)
