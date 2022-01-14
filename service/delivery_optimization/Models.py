from numpy import product
from numpy.core.fromnumeric import prod

import pandas as pd
from sklearn import linear_model
import datetime
from statsmodels.tsa.arima.model import ARIMA
import warnings
from statsmodels.tools.sm_exceptions import ConvergenceWarning
warnings.simplefilter('ignore', ConvergenceWarning)

class Models:
    def __init__(self, database_path):
        self.database_path = database_path
        self.sessions_df = self.read_training_data(database_path + "/sessions.jsonl", 'session_id')
        self.products_df = self.read_training_data(database_path + "/products.jsonl", 'product_id')
        self.weeks_df = self.convert_date_to_week_set()
        self.models = {"A": {}, "B": {}}
        self._initialize_models()

    def read_training_data(self, data_path, idx):
        df = pd.read_json(data_path, lines=True)
        df.set_index(idx, inplace=True)
        return df

    def convert_date_to_week_set(self):
        dates = self.sessions_df['timestamp']
        dates = pd.to_datetime(dates)
        dates = dates.dt.to_period('W')
        dates = dates.drop_duplicates()
        dates = dates.sort_values()
        return dates.values

    def _initialize_models(self):
        for product_id in self.products_df.index:
            self.models["A"][product_id] = ModelA(self.weeks_df, self.sessions_df[self.sessions_df['product_id'] == product_id])
            self.models["B"][product_id] = ModelB(self.weeks_df, self.sessions_df[self.sessions_df['product_id'] == product_id])

    def update_models(self):
        self.sessions_df = self.read_training_data(self.database_path + "/sessions.jsonl", 'session_id')
        self._initialize_models()

    def calculate_week_number(self, date_for_prediction=None):
        if date_for_prediction is None:
            date = datetime.date.today()
        else:
            date = datetime.datetime.strptime(date_for_prediction, "%d-%m-%Y").date()
        first_date = self.weeks_df[0].start_time.date()
        return (date - first_date).days // 7

    def get_predictions(self, group, products_id, date):
        if group not in self.models.keys():
            return None
        products_id = list(set(products_id).intersection(self.products_df.index))
        week_number = self.calculate_week_number(date)
        predictions = {}
        for product_id in products_id:
            predictions[product_id] = self.models[group][product_id].get_prediction(week_number)
        return predictions, week_number
    
    def get_all_predictions(self, group, date):
        products_id = self.products_df.index
        return self.get_predictions(group, products_id, date)

class ModelA:
    def __init__(self, weeks_df, sessions_df):
        self.weeks_df = weeks_df
        weeks_range = self.prepare_weeks_range()
        bought_products = self.product_bought(sessions_df)
        self.model = self.train(weeks_range, bought_products)

    def train(self, x, y):
        model = linear_model.LinearRegression().fit(x, y)
        linear_model.LinearRegression(copy_X=True, fit_intercept=True, n_jobs=1, normalize=False)
        return model

    def prepare_weeks_range(self):
        weeks = pd.DataFrame(index=[self.weeks_df[i].start_time for i in range(len(self.weeks_df))])
        weeks['weeks_from_start'] = ((weeks.index - weeks.index[0]).days) // 7
        return weeks.values.reshape(-1, 1)

    def product_bought(self, sessions_df):
        product_amount = sessions_df[sessions_df['event_type'] == "BUY_PRODUCT"]
        time_list = [(self.weeks_df[i].start_time, self.weeks_df[i].end_time) for i in range(len(self.weeks_df))]
        return [product_amount['timestamp'].between(s, e).sum() for s, e in time_list]

    def get_prediction(self, week_number):
        return self.model.predict([[week_number]])[0]

class ModelB:
    def __init__(self, weeks_df, sessions_df):
        self.weeks_df = weeks_df
        self.bought_products = self.product_bought(sessions_df)
        self.model = self.fit_model(self.bought_products)

    def product_bought(self, sessions_df):
        product_amount = sessions_df[sessions_df['event_type'] == "BUY_PRODUCT"]
        time_list = [(self.weeks_df[i].start_time, self.weeks_df[i].end_time) for i in range(len(self.weeks_df))]
        return [product_amount['timestamp'].between(s, e).sum() for s, e in time_list]

    def fit_model(self, dataset):
        model = ARIMA(dataset, order=(1, 1, 1))
        model_fit = model.fit()
        return model_fit

    def add_empty_rows(self, data_list, amount):
        return data_list + [0] * amount

    def get_prediction(self, week_number):
        if week_number > len(self.bought_products):
            self.bought_products += [0] * (week_number - len(self.bought_products))
        forecast = self.model.predict(start=week_number, end=week_number, dynamic=True)
        return forecast[0]

    def product_viewed(self, product_id, df, dates):
        viewed = df[(df['event_type'] == "VIEW_PRODUCT") & (df['product_id'] == product_id)]
        product_amount = df[(df['event_type'] == "BUY_PRODUCT") & (df['product_id'] == product_id)]
        daterange_df = pd.DataFrame()
        time_list = [(dates.values[i].start_time, dates.values[i].end_time) for i in range(len(dates))]
        daterange_df['count'] = [product_amount['timestamp'].between(s, e).sum() for s, e in time_list]
        daterange_df['viewed'] = [viewed['timestamp'].between(s, e).sum() for s, e in time_list]
        daterange_df['price'] = list(self.product_df[self.product_df.index == 1114]['price'])[0]
        daterange_df['discount'] = 0
        keys = product_amount.index
        for i, time in enumerate(product_amount['timestamp']):
            product_amount['timestamp'][keys[i]] = self.calculate_week_number(time.date())
        keys = viewed.index
        for i, time in enumerate(viewed['timestamp']):
            viewed['timestamp'][keys[i]] = self.calculate_week_number(time.date())
        keys_t = list(viewed['timestamp'])
        j = 0
        for i in daterange_df.index:
            if i in keys_t:
                daterange_df['discount'][i] = viewed['offered_discount'][keys[j]]
                j += 1
        return daterange_df

    def predict_products_multivar(self, sessions_df, week_number, y = None):
        products_predictions = {}
        product_list = list(sessions_df['product_id'])
        product_list = list(dict.fromkeys(product_list))
        df, dates = self.prepare_dataframe(sessions_df)
        product = 1114
        if y is None:
            y = self.product_viewed(product, sessions_df, dates)
        train, test = self.split_data(y)
        model_fit = self.fit_model(train['count'])
        predicted = self.predict(week_number-1, week_number+1, train, model_fit)
        products_predictions[product] = predicted['forecast'][week_number]
        return products_predictions, test

    def multi_var_arima(self, sessions_df, product, week_number):
        df, dates = self.prepare_dataframe(sessions_df)
        z = self.product_viewed(product, sessions_df, dates)
        z['wsp_sprzedazy'] = z['count']*z['price']*z['discount']
        z['wsp_wyswietlen'] = z['viewed']*z['price']*z['discount']
        pred, test = self.predict_products_multivar(sessions_df, week_number, z)
        return pred, test

    def pred_all_products(self, sessions_df, week_number):
        products_predictions = {}
        product_list = list(sessions_df['product_id'])
        product_list = list(dict.fromkeys(product_list))
        for product in product_list:
            pred, test = self.multi_var_arima(sessions_df, product, week_number)
            products_predictions[product] = pred
        return products_predictions
