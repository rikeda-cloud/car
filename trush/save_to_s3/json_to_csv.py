import glob
import json
import datetime

def _extract_schema(data: dict, schema: list[str]):
    result = []
    for attr in schema:
        try:
            value = data[attr]
            result.append(str(value))
        except:
            pass
    return result


def json_to_list(files: list[str], schema: list[str]):
    data = []
    for file in files:
        with open(file, 'r') as f:
            extracted_data = _extract_schema(json.load(f), schema)
            if extracted_data:
                data.append(extracted_data)
    return data

def write_data_to_csv(file: str, data:list[list], schema_size: int):
    with open(file, 'w') as f:
        for record in data:
            if len(record) == schema_size:
                f.write(",".join(record) + '\n')

def main():
    files = glob.glob("./*.json")
    schema = ["message", "test"]
    data = json_to_list(files, schema)
    dt_now = datetime.datetime.now()
    save_file = dt_now.strftime('%Y-%m-%d-%H-%M-%S-%f-') + '.csv'
    write_data_to_csv(save_file, data, len(schema))

if __name__ == "__main__":
    main()
