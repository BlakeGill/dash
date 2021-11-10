import requests
import json
from .query_builder import InfluxQueryBuilder
import pandas as pd


class InfluxCoreException(Exception):
    pass


class InfluxCoreClient:
    def __init__(self, host: str):
        self.host = host

    def upload_file(self, bucket: str, file_type: str, path: str):
        """
        Uploads data file directly to the influx core service.
        """
        print(bucket)
        res = requests.post(f"{self.host}/api/{bucket}/{file_type.upper()}/upload/datafile",
                            files={'file': open(path, "rb")})
        json_ = json.loads(res.content)
        if json_["error"]:
            raise InfluxCoreException(json_["message"])
        return res.status_code

    def query(self, query: InfluxQueryBuilder):
        return json.loads(
            requests.post(f"{self.host}/api/query", data={"query": query.build()}).text)

    def query_dataframe(self, query: InfluxQueryBuilder):
        data = self.query(query)
        return pd.DataFrame(data, columns=data.keys())
