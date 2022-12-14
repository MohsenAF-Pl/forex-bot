import pandas as pd
import toolbox

class Instrument():
    def __init__(self, obj):
        self.name = obj['name']
        self.ins_type = obj['type']
        self.displayName = obj['displayName']
        self.pipLocation = pow(10, obj['pipLocation']) # -4 -> 0.0001
        self.marginRate = obj['marginRate']
        
    def __repr__(self):
        return str(vars(self))

    @classmethod
    def get_instruments_df(cls):
        return pd.read_pickle(toolbox.get_instruments_data_filename())


    @classmethod
    def get_instruments_list(cls):
        df = cls.get_instruments_df()
        return [Instrument(x) for x in df.to_dict(orient='records')]

    @classmethod
    def get_instrument_dict(cls):
        i_list = cls.get_instruments_list()
        i_keys = [x.name for x in i_list]
        return {k:v for (k,v) in zip(i_keys, i_list)}

    @classmethod
    def get_instrument_by_name(cls, pairname):
        d = cls.get_instrument_dict()
        if pairname in d:
            return d[pairname]
        else:
            return None
    @classmethod
    def get_pairs_from_string(cls, pair_str):
        existing_pairs = cls.get_instrument_dict().keys()
        pairs = pair_str.split(',')

        pair_list = []
        for p1 in pairs:
            for p2 in pairs:
                p = f"{p1}_{p2}"
                if p in existing_pairs:
                    pair_list.append(p)

        return pair_list

if __name__ == '__main__':
    #for k,v in Instrument.get_instrument_dict().items():
    #    print(k, v)
    # print(Instrument.get_instrument_by_name('EUR_USD'))
    print(Instrument.get_test_pairs('XAU,GBP,EUR,USD,CAD,JPY,NZD,CHF'))