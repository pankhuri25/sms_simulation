# Import necessary libraries
import datetime
import time
import json
import logstash
import yaml
import random
import logging
from kafka import KafkaConsumer

# Load configuration from 'app-config.yml'
with open('app-config.yml') as f:
    props = yaml.safe_load(f)

# Initialize the logger for the consumer
def init_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    
    # Configure the Logstash logger handler
    logstash_host, logstash_port = props['logstash_server'].split(':')
    logger.addHandler(logstash.TCPLogstashHandler(logstash_host, logstash_port, version=1))
    
    # Disable other loggers to focus on errors
    logging.getLogger().setLevel(logging.ERROR)
    return logger

logger = init_logger()

# Parameters for simulating random wait times and failure rates
consumer_random_wait_time_params = props['consumer_random_wait_time_params']
consumer_random_failure_rate_params = props['consumer_random_failure_rate_params']
consumer_failure_rate = int(random.gauss(*consumer_random_failure_rate_params))
failure_msgs_index = set(random.sample(range(100), consumer_failure_rate)
message_count = 0

# Create a function to generate log data for messages
def get_log_data(message, status):
    return {
        'message_id': message['message_id'],
        'status': status,
        'phone_number': message['phone_number'],
        'event_end_time': datetime.datetime.now().isoformat()
    }

# Simulate sending a message to an actual customer
def send_message_to_api_for_actual_delivery(message):
    global message_count
    message_count = (message_count + 1) % 100
    random_wait_time = random.gauss(*consumer_random_wait_time_params)
    print("Triggering message to actual customer.", random_wait_time)
    time.sleep(random_wait_time)

    if message_count in failure_msgs_index:
        # Log an error message for failed message delivery
        logger.error(f"Message delivery to end client failed", extra=get_log_data(message, 'FAILED'))
        return False

    # Log a success message for messages successfully sent
    logger.info(f"Message successfully sent to mobile number", extra=get_log_data(message, 'SENT_TO_CLIENT'))
    return True

# Message processing function
def process_message(message):
    message = message.value.decode("utf-8")
    try:
        message = json.loads(message)
        # Log a message when a message is successfully consumed
        logger.info("Message successfully received at consumer", extra=get_log_data(message, 'CONSUMED'))
        send_message_to_api_for_actual_delivery(message)
    except Exception as e:
        # Log an error for failed message parsing
        logger.error(f"Message parsing failed for {message}")

# Initialize the Kafka consumer and start consuming messages
def init_consumer():
    consumer = None
    while consumer is None:
        try:
            consumer = KafkaConsumer(props['kafka_topic'],
                                     bootstrap_servers=props['bootstrap_servers'],
                                     max_poll_interval_ms=props['max_poll_interval_ms'],
                                     group_id=props['consumer_group_id'])
            time.sleep(5)
        except:
            pass

    # Start consuming messages and processing them
    for message in consumer:
        process_message(message)

# Start the Kafka consumer
init_consumer()