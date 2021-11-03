class channel:
    # eg: Ch001
    name = ""

    # eg: accrest_g, accpeak_g ...
    parameters = []

    def AddParameter(self, _parameter):
        # name is the channel name
        self.parameters.append(parameter)

    def SetName(self, _name):
        self.name = _name

    def __init__(self, _name):
        self.name = _name
