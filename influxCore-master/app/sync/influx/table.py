from collections import defaultdict


class Table:
    """
    Builds and corrects data to allow for easy insertion into a dataframe. Assumes all data inserted must be of the
    measurement.

        Typical usage example:

        table = TabularStructure()
        table.insert("2020-01-23 12:49:09", "VISA", "A1_A3_frf_coh_18250", 0.07695700000000001)
        table.insert("2020-01-23 12:49:29", "VISA", "A1_A3_frf_coh_5750", 0.039731)
        ....
        t = table.build()
    """

    def __init__(self):
        self.asset = None
        self.fields = set()
        self.index = defaultdict(list)  # {"timestamp": [field0, field1, fieldN, ...]}
        self.data = defaultdict(list)  # {"timestamp": [{"measurement": "AMU", "field": "mean", "value": "01"}, ...]}
        self.corrected = False

    def insert(self, timestamp: str, measurement: str, field: str, value: float):
        """
        Insert entry into table. The entry is inserted into the internal index and data structure.
        If the table has already been built all subsequent inserts are ignored.
        """
        if self.corrected:
            return
        if self.asset is None:
            self.asset = measurement
        self.data[timestamp].append({"field": field, "value": value})
        self.index[timestamp].append(field)
        self.fields.add(field)

    def __correct(self):
        """Pads out internal data structure.

        Compares fields and times stamps, if there are fields that don't have values at specific time stamps into the
        table a None value is inserted in this position to ensure all columns have the same length.

        Function can only be called once.
        """
        if self.corrected:
            return
        self.corrected = True
        for k, v in self.index.items():
            missing_fields = list(self.fields - set(v))
            if len(missing_fields) > 0:
                for field in missing_fields:
                    self.data[k].append({"field": field, "value": None})

    def build(self):
        """Builds final table like data structure.

        Returns:
            A dict with the tabular structure:

            {"timestamp": [time0, time1, timeN, ...],
            "asset": [a, a, a, ...],
            "field0": [v0, v1, vN, ...],
            "field1": [v0, v1, vN, ...],
            "fieldN": [v0, v1, vN, ...],
            ...}
        """
        self.__correct()
        base = defaultdict(list)
        for k, v in self.data.items():
            # base["timestamp"].append(pandas.to_datetime(k))
            base["timestamp"].append(k)
            base["asset"].append(self.asset)
            for i in v:
                base[i["field"]].append(i["value"])
        return dict(base)
