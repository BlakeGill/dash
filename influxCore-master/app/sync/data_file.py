"""
Schema for data files:

buckets -> condition, process, maintenance, analytics
measurement -> asset name e.g AMU
fields -> values to write

"""
from datetime import datetime
from typing import Iterator
from abc import ABC, abstractmethod

from fastapi import UploadFile

from .influx.influx_wrapper import InfluxWriteWrapper

ENCODING = "Windows-1252"


class DataFile(ABC):
    """Abstract base class defines functions to create a compatible data processor.
    for each new asset a separate class needs to be created and bespoke parsing functions
    implemented.
    """
    def __init__(self, asset: str, file: UploadFile):
        self.file = file.file
        self.asset = asset

    @abstractmethod
    def parse_entries(self) -> Iterator:
        """
        return: Iterator of parsed time stamps with headers and values zipped into a dictionary
        """
        ...

    @abstractmethod
    def _parse_time_stamp(self, fields: dict) -> datetime:
        """Extracts time stamp from string and store into datetime object.
        """
        ...

    def correct_types(self, fields: dict) -> dict:
        """
        defaults everything to float to avoid type collisions in db
        """
        for k, v in fields.items():
            try:

                fields[k] = float(v)
            except ValueError:
                fields[k] = 0.0
        return fields

    def write_to_db(self, bucket, writer: InfluxWriteWrapper):
        for time_stamp, fields in self.parse_entries():
            writer.write(bucket, self.asset, time_stamp, fields)
        writer.flush()


class AMUDataFile(DataFile):
    IGNORED_HEADERS = ['AMU-IP', 'TCPIP-Status', 'SCADA-Status', 'DAQ-Status', 'UDP-Status',
                       'CPU-Status', 'RAM-Status', 'HD-Status', 'FIFO-Status', 'AMU-Temp',
                       'RestartNo', 'AlarmNo', 'PreAlarmNo', 'Operating-State', 'Measuring-State',
                       'Ch000-Status', 'Ch001-Status', 'Ch002-Status', 'Ch003-Status', 'Ch004-Status',
                       'Ch005-Status', 'Ch006-Status', 'Ch007-Status', 'Ch008-Status', 'Ch009-Status',
                       'Ch010-Status', 'Ch011-Status', 'Ch012-Status', 'Ch013-Status', 'Ch014-Status',
                       'Ch015-Status', 'Ch016-Status', 'Equipment-Status', 'Operating-Class', 'Speed_rpm']

    def __init__(self, asset: str, file: UploadFile):
        super().__init__(asset, file)

    def parse_entries(self):
        """Split headers and group each row.
        """
        headers = self.file.readline().decode(ENCODING).strip("\n").split("\t")
        for line in self.file.readlines():
            dict_ = dict(zip(headers, line.decode(ENCODING).strip("\n").split("\t")))
            for item in self.IGNORED_HEADERS:
                dict_.pop(item, None)
            time_stamp = self._parse_time_stamp(dict_["Date Time"])
            dict_.pop("Date Time")
            yield time_stamp, self.correct_types(dict_)

    def _parse_time_stamp(self, time_stamp: str) -> datetime:
        tokens = time_stamp.split(" ")
        tokens[0] = tokens[0].replace(".", "-")
        return datetime.fromisoformat(" ".join(tokens))


class VISADataFile(DataFile):
    """
    , are replaced with . in values

    e.g.
    {"A1_median: "0,18447"} -> is converted to -> {A1_median": "0.18447"}
    """
    IGNORED_HEADERS = ["FileId"]

    def __init__(self, asset: str, file: UploadFile):
        super().__init__(asset, file)

    def parse_entries(self) -> Iterator:
        headers = self.file.readline().decode(ENCODING).strip("\n").strip("\r").split(";")
        for line in self.file.readlines():
            dict_ = dict(zip(headers, line.decode(ENCODING).strip("\n").strip("\r").split(";")))
            time_stamp = self._parse_time_stamp(dict_)
            dict_.pop("Date_Time")
            for item in self.IGNORED_HEADERS:
                dict_.pop(item, None)
            fields = {k: v.replace(",", ".") for k, v in dict_.items()}  # replace , with . for decimals
            yield time_stamp, self.correct_types(fields)

    def _parse_time_stamp(self, fields: dict) -> datetime:
        return datetime.fromisoformat(fields["Date_Time"])
