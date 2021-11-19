import json
import os

import redis

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")


class ConfigStore:
    """Cluster configuration store backed by Redis.
    Primary purpose is the store the address of all the other nodes in the cluster.
    Redis allows for the information to be persisted across multiple isolated processes in a single node.
    """

    def __init__(self):
        self.client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

    def get_influx_nodes(self) -> set:
        """Return set of Influx db hosts in config store
        """
        ret = self.client.get("influx_nodes")
        if ret is None:
            return set()
        return set(json.loads(ret))

    def add_influx_node(self, node: str):
        """Append Influx DB node to config store
        """
        current_nodes = self.get_influx_nodes()
        current_nodes.add(node)
        self.client.set("influx_nodes", json.dumps(list(current_nodes)))

    def remove_influx_node(self, node: str):
        """Remove Influx db node from config store
        """
        current_nodes = self.get_influx_nodes()
        current_nodes.remove(node)
        self.client.set("influx_nodes", json.dumps(current_nodes))
