"""
Visual tests to understand how to consume the API, these are not a replacement for unit tests.
"""
import os
import sys
import time
from timeit import default_timer as timer
import functools

from client.query_builder import InfluxQueryBuilder
from client.influx_client import InfluxCoreClient

ENCODING = "Windows-1252"
server = "http://localhost:8000"

AMU_FILE = "./resources/AMU_10.201.161.151_StatusFile_20160817_21.txt"
VISA_FILE = "./resources/VISA_Parameters_20200123_124859.csv"
VISA_FILES = "/Users/asad/Downloads/Imported/VISA"
FEATURE_FILE = "./resources/FeatureTable_ALL.csv"

client = InfluxCoreClient(server)


def time_function(func):
    @functools.wraps(func)
    def stub(*args, **kwargs):
        start = timer()
        ret = func(*args, **kwargs)
        end = timer()
        print(f"Time Taken: {end - start}s", file=sys.stderr)
        return ret

    return stub


def write_to_csv(data):
    print(data.to_csv(), file=open("VISA_new.csv", "w"))


def get_files_in_directory(path):
    for filename in os.listdir(path):
        yield filename


def upload():
    #print(client.upload_file("process", "AMU", AMU_FILE))
    #print(client.upload_file("process", "VISA", VISA_FILE))
    print(client.upload_file("process", "VISA", FEATURE_FILE))

def upload_VISA_directory():
    for file in get_files_in_directory(VISA_FILES):
        if file.endswith("csv"):
            print(file)
            print(client.upload_file("process", "VISA", VISA_FILES + "/" + file))


@time_function
def AMU_query():
    return client.query_dataframe(InfluxQueryBuilder("process").range().asset("AMU"))


@time_function
def VISA_query():
    return client.query_dataframe(InfluxQueryBuilder("process").range().asset("VISA"))


if __name__ == '__main__':
    print("Upload Test: Uploading files to influx ETL app", file=sys.stderr)
    upload()
    print("Upload Test: Waiting 10 seconds for all batch processes on server side to complete.", file=sys.stderr)
    time.sleep(10)

    print("Query Test: Querying all fields from AMU assets and loading into data frame", file=sys.stderr)
    #print(AMU_query())
    print("Query Test: Querying all fields from VISA assets and loading into data frame", file=sys.stderr)
    print(VISA_query())
