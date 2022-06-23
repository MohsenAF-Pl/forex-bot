import pandas as pd
import utils

class Instrument():
    def __init__(self, ob):
        self.name = ob['name']
        self.instrument_type = ob['type']
        self.displayName = ob['displayName']
        self.pipLocation = pow(10, ob['pipLocation']) # -4 -> 0.0001
        self.marginRate = ob['marginRate']

# actually this function makes the result of this file readable and usable
    def __repr__(self):
        return str(vars(self))

    @classmethod
    # we use the utils function to load the data we have saved before
    def get_instruments_df(cls):
        return pd.read_pickle(utils.get_instruments_data_filename())

    @classmethod
    def get_instruments_list(cls):
        df = cls.get_instruments_df()
        return [Instrument(x) for x in df.to_dict(orient='records')]


    @classmethod
    def get_instruments_dict(cls):
        i_list = cls.get_instruments_list()
        i_keys = [x.name for x in i_list]
        return { k:v for (k,v) in zip(i_keys, i_list) }

    
    @classmethod
    def get_instrument_by_name(cls, pairname):
        d = cls.get_instruments_dict()
        if pairname in d:
            return d[pairname]
        else:
            return None


if __name__ == "__main__":
    # for k,v in Instrument.get_instruments_dict().items():
    #     print(k,v)
    print(Instrument.get_instrument_by_name("EUR_USD"))
