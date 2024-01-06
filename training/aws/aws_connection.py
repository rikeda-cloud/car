import pub


class AwsConnection():
    def __init__(self):
        self.connection = pub.connect_aws()
 
    def send(self, data):
        pub.pub_data(self.connection, data)

    def disconnect(self):
        pub.disconnect_aws(self.connection)

    def __del__(self):
        self.disconnect()
