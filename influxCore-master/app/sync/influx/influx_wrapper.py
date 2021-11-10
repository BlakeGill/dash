import itertools
import os
from timeit import default_timer

import requests
from influxdb_client import InfluxDBClient, Point, Dialect
from influxdb_client.client.write_api import WriteOptions

from .replicas import Replicas
from .table import Table

INFLUX_URL = os.getenv("INFLUXDB_V2_URL")
ORGANISATION = os.getenv("INFLUXDB_V2_ORG")
TOKEN = os.getenv("INFLUXDB_V2_TOKEN")


def get_client():
    return InfluxDBClient(url=INFLUX_URL, org=ORGANISATION, token=TOKEN)


class InfluxWriteWrapper:
    @staticmethod
    def get_instance():
        return InfluxWriteWrapper(get_client())

    def __init__(self, client: InfluxDBClient):
        self.writer = client.write_api(write_options=WriteOptions(batch_size=50_000, flush_interval=10_000))
        self.replicas = Replicas(ORGANISATION, TOKEN)

    def write(self, bucket: str, measurement: str, time: str, fields: dict, tags: dict = None):
        record_ = Point(measurement).time(time)
        for k, v in fields.items():
            record_.field(k, v)
        if tags is not None:
            for k, v in tags.items():
                record_.tag(k, v)
        # write to local instance first then replicas
        self.writer.write(bucket=bucket, record=record_)
        self.replicas.write(bucket, record_)

    def flush(self):
        self.writer.flush()


class InfluxReadWrapper:
    @staticmethod
    def get_instance():
        return InfluxReadWrapper(get_client())

    def __init__(self, client: InfluxDBClient):
        self.reader = client.query_api()

    def tabulate_output(self, csv_buffer: list) -> dict:
        """Structure output into table
        Args:
            csv_buffer: list buffer containing lines of parsed csv.

        Returns:
            Dict object in a table like structure containing data from csv buffer.
        """
        table = Table()
        if len(csv_buffer) < 3:
            return {}
        headers = csv_buffer[0]
        for line in itertools.islice(csv_buffer, 1, None):
            dict_ = dict(zip(headers, line))
            try:
                table.insert(dict_["_time"], dict_["_measurement"], dict_["_field"], float(dict_["_value"]))
            except ValueError:
                table.insert(dict_["_time"], dict_["_measurement"], dict_["_field"], dict_["_value"])
            except KeyError:
                pass
        return table.build()

    def read(self, query: str) -> dict:
        """Send query to db through client and return tabulated output

        Args:
            query: FluxQL query to send to database

        Returns:
            Dictionary object containing result of query

        TODO: remove debug timer
        """
        start = default_timer()
        data = list(self.reader.query_csv(query, dialect=Dialect()))
        end = default_timer()
        print(f"DB READ TIME {end - start}s")
        return self.tabulate_output(data)


class InfluxUtils:
    """TODO: Currently unused
    """

    @staticmethod
    def get_instance():
        return InfluxUtils(get_client())

    def __init__(self, client: InfluxDBClient):
        self.buckets_api = client.buckets_api()

    def delete_bucket(self, name):
        self.buckets_api.delete_bucket(name)

    def create_bucket(self, name):
        self.buckets_api.create_bucket(name)

    def delete_entries(self, bucket, start, stop):
        res = requests.post(
            f"{INFLUX_URL}/api/v2/delete/?org={ORGANISATION}&bucket={bucket}",
            headers={
                "Authorization": f"Token {TOKEN}"},
            data={
                "start": start,
                "stop": stop
            })
        return res.status_code
