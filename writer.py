import boto3
import sys
import getopt
import time
import json

client = boto3.Session(region_name='ap-south-1').client(
    'kinesis', aws_access_key_id='x', aws_secret_access_key='x',
    endpoint_url='http://localhost:4567')


def create_stream(streamName):
    streams = client.list_streams()
    if streamName not in streams['StreamNames']:
        client.create_stream(StreamName=streamName, ShardCount=1)
        time.sleep(1)


def publish_stream(stream, data):
    response = client.put_record(
        StreamName=stream, Data=json.dumps(data), PartitionKey='test')
    print(response)


def main(argv):
    streamName = ''
    data = ''
    try:
        opts, args = getopt.getopt(argv, "h", ["streamName=", "data="])
    except getopt.GetoptError:
        print('writer.py --streamName <stream-name> --data <json-data>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('writer.py --streamName <stream-name> --data <json-data>')
            sys.exit()
        elif opt in ("--streamName"):
            streamName = arg
        elif opt in ("--data"):
            data = arg

    print('streamName:', streamName)
    print('data:', data)

    create_stream(streamName)
    publish_stream(streamName, json.loads(data))

if __name__ == "__main__":
    main(sys.argv[1:])
