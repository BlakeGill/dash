from ..config.config_store import ConfigStore
from influxdb_client import InfluxDBClient, WriteOptions


class Replicas:
    """Manages writes to replicas.

     Main focus is writes, error handling and recovery processes.
    """

    def __init__(self, org, token):
        self.org = org
        self.token = token
        self.config = ConfigStore()

    @property
    def nodes(self) -> list:
        return list(self.config.get_influx_nodes())

    def __get_writer(self, node):
        return InfluxDBClient(url=node, org=self.org, token=self.token) \
            .write_api(write_options=WriteOptions(batch_size=50_000, flush_interval=10_000))

    def write(self, bucket, record):
        """Write data to all replicas
        """
        for node in self.nodes:
            try:
                self.__get_writer(node).write(bucket=bucket, record=record)
            except IOError as e:
                self.on_error(node, bucket, record)
                raise IOError(e)

    def on_error(self, node, bucket, record):
        """Setup write buffer for specific node until it comes back.
        Dispatches watcher process to keep eye on Node if it comes back.
        After 3 failed writes the node is dropped.
        """
        print(f"{node} has failed to respond")
