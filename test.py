import logging
import logstash
import sys

host = 'localhost'

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logstash.TCPLogstashHandler(host, 5959, version=1))
logger.addHandler(logstash.TCPLogstashHandler(host, 5959, version=1))

# add extra field to logstash message
extra = {
    'test_string': 'python version: ' + repr(sys.version_info),
    'test_boolean': True,
    'test_dict': {'a': 1, 'b': 'c'},
    'test_float': 1.23,
    'test_integer': 123,
    'test_list': [1, 2, '3'],
}
logger.info('INFO', extra=extra)
