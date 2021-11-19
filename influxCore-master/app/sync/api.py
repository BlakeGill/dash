import requests
from fastapi import UploadFile

from .influx.influx_wrapper import InfluxReadWrapper, InfluxWriteWrapper
from .config.config_store import ConfigStore
from .data_file import AMUDataFile, VISADataFile

ENCODING = "Windows-1252"
ASSET_MAPPING = {"AMU": AMUDataFile,
                 "VISA": VISADataFile}


class InfluxAPI:
    """
    Ties directly into the http server and unifies backend functionalities under one class.
    Handles errors and returns
    """

    def __init__(self):
        self.config = ConfigStore()

    def get_influx_nodes(self):
        """Return list of influx nodes in config store.
        """
        return self.config.get_influx_nodes()

    def send_remote_node_host_ip(self, node):
        """Send node host ip address.
        """
        requests.post(f"http://{node}:8000/api/config/add/node", data={"node": None,
                                                                       "respond": False})

    def add_influx_node(self, node):
        """Writes new influx node to config store then sends its own IP to the node.
        """
        self.config.add_influx_node(node)

    def ingest_data_file(self, bucket, asset, file: UploadFile):
        """Selects the correct class to process the datafile and writes processed data to database.
        """
        try:
            ASSET_MAPPING[asset](asset, file).write_to_db(bucket, InfluxWriteWrapper.get_instance())
            return {"error": False, "message": ""}
        except KeyError:
            return {"error": True, "message": f"Asset {asset} not yet supported"}

    def send_raw_query(self, query):
        """
        TODO: handle Errors
        """
        return InfluxReadWrapper.get_instance().read(query)
