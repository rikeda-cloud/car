from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import time as t
import json

# Define ENDPOINT, CLIENT_ID, PATH_TO_CERTIFICATE, PATH_TO_PRIVATE_KEY, PATH_TO_AMAZON_ROOT_CA_1, MESSAGE, TOPIC, and RANGE
ENDPOINT = "a1jmtdvz0m9ze3-ats.iot.ap-northeast-1.amazonaws.com"
CLIENT_ID = "testDevice"
PATH_TO_CERTIFICATE = "./cert/rs-certificate.pem.crt"
PATH_TO_PRIVATE_KEY = "./cert/rs-private.pem.key"
PATH_TO_AMAZON_ROOT_CA_1 = "./cert/AmazonRootCA1.pem"
MESSAGE = "Hello World"

def connect_aws():
# Spin up resources
    event_loop_group = io.EventLoopGroup(1)
    host_resolver = io.DefaultHostResolver(event_loop_group)
    client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
    mqtt_connection = mqtt_connection_builder.mtls_from_path(
                endpoint = ENDPOINT,
                cert_filepath = PATH_TO_CERTIFICATE,
                pri_key_filepath = PATH_TO_PRIVATE_KEY,
                client_bootstrap = client_bootstrap,
                ca_filepath = "./cert/AmazonRootCA1.pem",
                client_id = CLIENT_ID,
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

def pub_data(mqtt_connection ,message, topic):
    mqtt_connection.publish(topic=topic, payload=json.dumps(message), qos=mqtt.QoS.AT_LEAST_ONCE)
    print("Published: '" + json.dumps(message) + "' to the topic: " + str(topic))
    t.sleep(0.1)

def disconnect_aws(mqtt_connection):
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()

# 証明書など接続を確認するメソッド
RANGE = 2
TOPIC = "test/testing"

def test():
    mqtt_connection = connect_aws()
    for i in range (RANGE):
        message = {"message" : "{} [{}]".format(MESSAGE, i+1)}
        pub_data(mqtt_connection, message, TOPIC)
    print('Publish End')
    disconnect_aws(mqtt_connection)

# test()