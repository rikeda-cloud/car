from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import time as t
import json

# Define ENDPOINT, CLIENT_ID, PATH_TO_CERTIFICATE, PATH_TO_PRIVATE_KEY, PATH_TO_AMAZON_ROOT_CA_1, MESSAGE, TOPIC, and RANGE
ENDPOINT = "customEndpointUrl"
CLIENT_ID = "testDevice"
PATH_TO_CERTIFICATE = "certificates/a1b23cd45e-certificate.pem.crt"
PATH_TO_PRIVATE_KEY = "certificates/a1b23cd45e-private.pem.key"
PATH_TO_AMAZON_ROOT_CA_1 = "certificates/root.pem"
MESSAGE = "Hello World"
TOPIC = "test/testing"
RANGE = 20

def connect_aws():
# Spin up resources
    event_loop_group = io.EventLoopGroup(1)
    host_resolver = io.DefaultHostResolver(event_loop_group)
    client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
    mqtt_connection = mqtt_connection_builder.mtls_from_path(
                endpoint="a1jmtdvz0m9ze3-ats.iot.ap-northeast-1.amazonaws.com",
                cert_filepath="./cert/rs-certificate.pem.crt",
                pri_key_filepath="./cert/rs-private.pem.key",
                client_bootstrap=client_bootstrap,
                ca_filepath="./cert/AmazonRootCA1.pem",
                client_id="test",
                clean_session=False,
                keep_alive_secs=6
                )
    print("Connecting to {} with client ID '{}'...".format(
            ENDPOINT, CLIENT_ID))
    # Make the connect() call
    connect_future = mqtt_connection.connect()
    # Future.result() waits until a result is available
    connect_future.result()
    print("Connected!")
    # Publish message to server desired number of times.
    return mqtt_connection


def pub_data(mqtt_connection ,message):
    mqtt_connection.publish(topic=TOPIC, payload=json.dumps(message), qos=mqtt.QoS.AT_LEAST_ONCE)
    print("Published: '" + json.dumps(message) + "' to the topic: " + "'test/testing'")
    t.sleep(0.1)

def disconnect_aws(mqtt_connection):
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()


def test():
    mqtt_connection = connect_aws()
    for i in range (RANGE):
        message = {"message" : "{} [{}]".format(MESSAGE, i+1)}
        pub_data(mqtt_connection, message)
    print('Publish End')
    disconnect_aws(mqtt_connection)
