import time
import pub

TOPIC = "training"

class AwsDataModule():
    
    def __init__(self):
        self.mqtt_connection = pub.connect_aws()
        return
        
    def send(self, message):
        try:
            pub.pub_data(self.mqtt_connection, message, TOPIC)
        except KeyboardInterrupt:
            print('stop!')
            pub.disconnect_aws(self.mqtt_connection)
        return

    def __del__(self):
        pub.disconnect_aws(self.mqtt_connection)
        return

def send_data(message):
    mqtt_connection = pub.connect_aws()
    try:
        pub.pub_data(mqtt_connection, message, TOPIC)
    
    except KeyboardInterrupt:
        print('stop!')
        pub.disconnect_aws(mqtt_connection)
    pub.disconnect_aws(mqtt_connection)

# data sending test

def send_data(message):
    mqtt_connection = pub.connect_aws()
    try:
        pub.pub_data(mqtt_connection, message, TOPIC)
    
    except KeyboardInterrupt:
        print('stop!')
        pub.disconnect_aws(mqtt_connection)
    pub.disconnect_aws(mqtt_connection)

def test():
    message = {
        "d_1" : '{0:.1f}'.format(1),
        "d_2" : '{0:.1f}'.format(2),
        "d_3" : '{0:.1f}'.format(3),
        "d_4" : '{0:.1f}'.format(4),
        "d_5" : '{0:.1f}'.format(5),
        "d_6" : '{0:.1f}'.format(6),
        "d_7" : '{0:.1f}'.format(7),
        "d_8" : '{0:.1f}'.format(8),
        "d_9" : '{0:.1f}'.format(9),
        "d_10" : '{0:.1f}'.format(10),
        "speed" : '{0:.1f}'.format(0),
        "handle" : '{0:.1f}'.format(0),
        "timestamp" : '{0:.1f}'.format(time.time())
    }
    send_data(message)
