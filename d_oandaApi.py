import requests
import pandas as pd
import authentication
import toolbox

class OandaApi():

    def __init__(self):
        self.session = requests.Session()

    def fetch_instruments(self):
        url = f"{authentication.OANDA_URL}/accounts/{authentication.ACCOUNT_ID}/instruments"
        response = self.session.get(url, params=None, headers=authentication.SECURE_HEADER)
        return response.status_code, response.json()

    def get_instruments_df(self):
        code ,data = self.fetch_instruments()
        if code ==200:
            df = pd.DataFrame.from_dict(data['instruments'])
            return df[['name', 'type', 'displayName', 'pipLocation', 'marginRate']]
        else:
            return None

    def save_instruments(self):
        df = self.get_instruments_df()
        if df is not None:
            df.to_pickle(toolbox.get_instruments_data_filename())
    
    # by default this returns 300 candles
    # we must provide the date as timestamp as int for OandaApi
    def fetch_candles(self, pair_name, count=None, granularity='H1', date_from=None, date_to=None):
        url = f"{authentication.OANDA_URL}/instruments/{pair_name}/candles"

        params = dict(
            granularity = granularity,
            price = "MBA"
        )

        if date_from is not None and date_to is not None:
            params['to'] = int(date_to.timestamp())
            params['from'] = int(date_from.timestamp())
        elif count is not None:
            params['count'] = count
        else:
            params['count'] = 300

        response = self.session.get(url, params=params, headers=authentication.SECURE_HEADER)

        if response.status_code != 200:
            return response.status_code, None

        return response.status_code, response.json()


if __name__ == '__main__':
    api = OandaApi()
    # api.save_instruments()

    date_from = toolbox.get_utc_dt_from_string('2019-05-05 18:00:00')
    date_to = toolbox.get_utc_dt_from_string('2019-07-05 18:00:00')
    print(api.fetch_candles('EUR_USD', date_from=date_from, date_to=date_to))