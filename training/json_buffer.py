import datetime
import json
import os
import data_utils.send_data

class JsonBuffer():
    def __init__(self):
        self.save_dir = "./json/"
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
        self.buffer = []

    def is_empty(self) -> bool:
        return self.buffer == []

    def add(self, data: dict) -> None:
        self.buffer.append(data)

    def save(self) -> None:
        if self.is_empty():
            return
        dt_now = datetime.datetime.now()
        file = self.save_dir + dt_now.strftime('%Y%m%d%H%M%S') + '.json'
        with open(file, 'w') as f:
            json.dump(self.buffer, f)
        self.buffer = []

    def _get_json_files(self):
        return [
            self.save_dir + f
            for f in os.listdir(self.save_dir)
            if os.path.isfile(os.path.join(self.save_dir, f))
        ]

    def send_to_aws(self):
        aws_data_module = data_utils.send_data.AwsDataModule()
        json_files = self._get_json_files()
        for file in json_files:
            with open(file, 'r') as f:
                data_list = f.read()
                [aws_data_module.send(data) for data in data_list]
            os.unlink(file)
        os.rmdir(self.save_dir)


if __name__ == '__main__':
    buffer = JsonBuffer()
    buffer.send_to_aws()
