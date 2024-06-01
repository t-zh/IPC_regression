import pandas as pd
import numpy as np

def prepocessing_data(file_name):
    '''
    Fuction for loading data from rosstat_site, clearing data and conversion in a format
    with columns [months, year, ipc], where ipc is a target
    :param file_name: url
    :return: df(DataFrame)
    '''
    df = pd.read_excel(file_name, sheet_name=3, index_col=0, skiprows=[0, 1, 2, 4])
    df = df[df[df.columns[1]].notna()]
    df = df[:-1]

    df.index.name = 'month'
    df.reset_index(inplace=True)
    month2int = {month: idx + 1 for idx, month in enumerate(df['month'])}
    int2month = {idx + 1: month for idx, month in enumerate(df['month'])}
    df['month'] = df['month'].map(month2int)

    df = pd.melt(df, id_vars=['month'], value_vars=df.columns, var_name='year', value_name='ipc').dropna()

    df = df[50:]
    df['ipc'] = remove_outliers(df['ipc'])
    return df


def prepare_data_for_prediction(df):
    '''
    Function prepare data on which model makes predictions on 6 months:
    '''
    last_month = df['month'].iloc[-1]
    last_year = df['year'].iloc[-1]

    data = {'month': (np.array(range(last_month + 1, last_month + 7)))}
    X_pred = pd.DataFrame(data)
    X_pred['year'] = np.where(X_pred['month'] <= 12, last_year, last_year + 1)
    X_pred['month'] = np.where(X_pred['month'] % 12 != 0, X_pred['month'] % 12, 12)
    return X_pred

# Remove ouliers
def remove_outliers(data):
    '''
    Function finds outliers and changes it to boundaries of the acceptable interval Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
    :param data: DataFrame
    :return:  data DataFrame
    '''
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)

    IQR = Q3 - Q1

    data[(data < Q1 - 1.5 * IQR)] = Q1 - 1.5 * IQR
    data[(data > Q3 + 1.5 * IQR)] = Q3 + 1.5 * IQR
    return data

def prepare_data_for_plotting(df, X_pred, predictions, period_in_months):
    '''
    Function concatenated predictions and data ipc for the last period (period_in_months)

    '''
    int2month = {1: 'январь', 2: 'февраль', 3: 'март', 4: 'апрель', 5: 'май', 6: 'июнь', 7: 'июль', 8: 'август',
                 9: 'сентябрь', 10: 'октябрь', 11: 'ноябрь', 12: 'декабрь'}
    y_to_plot = pd.concat([df['ipc'], pd.DataFrame(np.round(predictions, 2))], axis=0).reset_index(drop=True)
    y_to_plot = y_to_plot.iloc[-period_in_months:]
    X_to_plot = pd.concat([df[['month', 'year']], X_pred], axis=0).reset_index(drop=True)
    X_to_plot['month_year'] = X_to_plot['month'].map(lambda x: int2month[x]) + ' ' + X_to_plot['year'].map(
        lambda x: str(x))
    X_to_plot = X_to_plot.iloc[-period_in_months:]
    return X_to_plot['month_year'], y_to_plot


def augument_data_by_exchange_rate(df):
    '''
    Fuтсtion loads data of exchange rate and adds to the main dataset
    :return: DataFrame with columns month, year, exchange rate, ipc
    '''

    df_exchange_rate = pd.read_xml('./data/exchange_rate.xml', parser="lxml")

    df_exchange_rate = df_exchange_rate.loc[:,["Date", "Value"]]
    df_exchange_rate.columns = ['date', 'exchange_rate']
    df_exchange_rate['exchange_rate'] = df_exchange_rate['exchange_rate'].str.replace(',', '.').astype(float).astype(float)
    df_exchange_rate['date'] = df_exchange_rate['date'].map(lambda x: x.replace('.', '/'))

    df_exchange_rate['date'] = pd.to_datetime(df_exchange_rate['date'], dayfirst=True)
    diff_in_month = df_exchange_rate['date'].iloc[-1].month - df['month'].iloc[-1]
    #group by months
    df_exchange_rate = df_exchange_rate.groupby(df_exchange_rate['date'].dt.to_period("M"))['exchange_rate'].mean()
    #make datasets the same length
    df_exchange_rate.drop(df_exchange_rate.tail(diff_in_month).index, inplace=True)

    df_exchange_rate = df_exchange_rate.tail(len(df)).reset_index(drop=True)
    df_augumented = pd.concat([df.reset_index(drop=True), df_exchange_rate], axis=1)
    return df_augumented

