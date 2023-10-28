# Import necessary libraries
import json
import random
import string
import yaml
import time
import logging
import logstash
import uuid
import datetime
from kafka.admin import KafkaAdminClient, NewTopic
from kafka import KafkaProducer

# Load configuration from 'app-config.yml'
with open('app-config.yml') as f:
    props = yaml.safe_load(f)

# Initialize the logger for the producer
def init_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    
    # Configure the Logstash logger handler
    logstash_host, logstash_port = props['logstash_server'].split(':')
    logger.addHandler(logstash.TCPLogstashHandler(logstash_host, logstash_port, version=1))
    
    # Disable other loggers to focus on errors
    logging.getLogger().setLevel(logging.ERROR)
    return logger

# Initialize the Kafka producer and logger
producer = None
logger = init_logger()

# Generate a random SMS message
def generate_random_sms():
    phone_number = "".join(random.choices(string.digits, k=10))
    message = "".join(random.choices(string.ascii_letters + string.digits, k=random.randint(1, 100)))
    message_id = str(uuid.uuid4())
    return {"phone_number": phone_number, "message": message, 'message_id': message_id}

# Create log data for the produced message
def get_log_data(message, status):
    return {
        'message_id': message['message_id'],
        'status': status,
        'phone_number': message['phone_number'],
        'event_start_time': datetime.datetime.now().isoformat()
    }

# Produce SMS messages to Kafka
def produce_sms_messages():
    global producer
    num_messages = props['no_of_msgs_in_batch']  # Number of SMS messages to produce
    
    if producer is None:
        producer = KafkaProducer(bootstrap_servers=props['bootstrap_servers'],
                                 value_serializer=lambda x: json.dumps(x).encode('utf-8'))
    
    for _ in range(num_messages):
        sms_message = generate_random_sms()
        producer.send(props['kafka_topic'], value=sms_message)
        print(f"Message sent: {sms_message}")
        
        # Log a success message for the produced message
        logger.info("Message successfully sent", extra=get_log_data(sms_message, 'PRODUCED'))
        
        # Delay the producer to mimic real-time production
        time.sleep(10)

# Create a Kafka topic
def create_topic():
    try:
        admin_client = KafkaAdminClient(
            bootstrap_servers=props['bootstrap_servers'],
            client_id=props['client_id']
        )

        topic_metadata = admin_client.list_topics()
        if props['kafka_topic'] not in topic_metadata:
            topic_list = []
            topic_list.append(NewTopic(name=props['kafka_topic'],
                                       num_partitions=props['partition_count'],
                                       replication_factor=props['replication_factor']))
            admin_client.create_topics(topic_list, validate_only=False)
        return True
    except Exception as e:
        print("Exception while creating topic", e)

# Main function to continuously produce messages
def produce():
    while True:
        try:
            create_topic()
            produce_sms_messages()
        except Exception as e:
            print(e)

# Start the producer
produce()