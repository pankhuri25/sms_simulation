import datetime
import time
import json
import logstash
import yaml
import random
import logging

from kafka import KafkaConsumer

with open('app-config.yml') as f:
    props = yaml.safe_load(f)

def init_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logstash_host, logstash_port = props['logstash_server'].split(':')
    logger.addHandler(logstash.TCPLogstashHandler(logstash_host, logstash_port, version=1))
    # Disable other loggers
    logging.getLogger().setLevel(logging.ERROR)
    return logger

logger = init_logger()
consumer_random_wait_time_params= props['consumer_random_wait_time_params']
consumer_random_failure_rate_params = props['consumer_random_failure_rate_params']
consumer_failure_rate = int(random.gauss(*consumer_random_failure_rate_params))
failure_msgs_index = set(random.sample(range(100), consumer_failure_rate))
message_count = 0

def get_log_data(message, status):
    return {
        'message_id': message['message_id'],
        'status': status,
        'phone_number': message['phone_number'],
        'event_end_time': datetime.datetime.now().isoformat()
    }

def send_message_to_api_for_actual_delivery(message):
    global message_count
    message_count = (message_count + 1) % 100
    random_wait_time = random.gauss(*consumer_random_wait_time_params)
    print("Triggering message to actual customer.", random_wait_time)
    time.sleep(random_wait_time)

    if message_count in failure_msgs_index:
        logger.error(f"Message delivery to end client failed", extra=get_log_data(message, 'FAILED'))
        return False

    logger.info(f"Message successfully sent to mobile number", extra=get_log_data(message, 'SENT_TO_CLIENT'))
    return True

def process_message(message):
    message = message.value.decode("utf-8")
    try:
        message = json.loads(message)
        logger.info("Message successfully received at consumer", extra=get_log_data(message, 'CONSUMED'))
        send_message_to_api_for_actual_delivery(message)
    except Exception as e:
        logger.error(f"Message parsing failed for {message}")


def init_consumer():
    # Create a KafkaConsumer instance
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
    # Start consuming messages
    for message in consumer:
        process_message(message)


init_consumer()

