# sms_simulation_project

### Objective

The objective is to simulate sending a large number of SMS alerts, like for an emergency alert service.
The simulation consists of three parts:
  1. A producer that generates a configurable number of messages (default 1000) to random phone
  numbers. Each message contains up to 100 random characters.
  2. A configurable number of senders who pick up messages from the producer and simulate
  sending messages by waiting a random period of time distributed around a configurable mean.
  Senders also have a configurable failure rate.
  3. A progress monitor that displays the following and updates it every N seconds (configurable):
      a. Number of messages sent so far
      b. Number of messages failed so far
      c. Average time per message so far
One instance each for the producer and the progress monitor will be started while a variable number of
senders can be started with different mean processing time and error rate settings. 
### How to run

The project is set in a docker-containerized environment and can be easily launched using the command:

`docker-compose up` 

All the configurations are present in `app-config.yml`

It will automatically download all the base images and will launch the necessary services. A Docker daemon has to be running for it. 
Download the Docker Desktop from here:
https://www.docker.com/products/docker-desktop/

Please see here for more details - https://docs.docker.com/compose/ 

Respective launched applications can be found at:

•	Kafka - <localhost:9092> (Inside containers it will be accessible as <kafka:29092>)

•	Logstash - http://localhost:5959/ 

•	Elasticsearch - http://localhost:9200/ 

•	Kibana - http://localhost:5601/ (Please import [‘export.ndjson’] file in Kibana to import dashboard analysis.)

There is a `requirements.txt` file which includes all the libraries and dependencies used with versions. These will be automatically installed when Docker is composed.
