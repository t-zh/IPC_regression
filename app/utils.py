import requests
import pandas as pd
from datetime import date
from plotly.subplots import make_subplots
import plotly.graph_objs as go
def download_file():
    #Индексы потребительских цен на товары и услуги по Российской Федерации, месяцы (с 1991 г.)
    data_file_path = '/storage/mediabank/ipc_mes_04-2024.xlsx'
    url = 'https://rosstat.gov.ru/'+ data_file_path

    response = requests.get(url)
    file_path = './data/ipc_mes.xlsx'
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print('File downloaded successfully')
    else:
        print('Failed to download file')
    return None

def plot_the_graph(X, y):
    fig = make_subplots(
           rows=1, cols=4,
           shared_xaxes=True,
           horizontal_spacing=0.1,
           row_heights=[100],
           vertical_spacing=0.5,
           subplot_titles=("", "Инедекс потребительских цен"),
           specs=[[{"type": "table"},
                  {"colspan": 3}, None, None]])


    table = pd.concat([X.reset_index(drop=True), y.bfill(axis=1).iloc[:, 0].transpose().reset_index(drop=True)], axis=1).iloc[::-1]

    fig.add_trace(go.Table(cells=dict(values=table.transpose())), row=1, col=1)
    fig.add_trace(go.Scatter(x=X, y=y[0], mode='markers', name='ИПЦ'), row=1, col=2)
    # fig.add_trace(go.Scatter(x=X, y=y['ipc'], mode='markers', name='ИПЦ'), row=1, col=2)
    fig.update_layout(title_text='Индекс потребительских цен',
                     legend=dict(yanchor="bottom", orientation="h"),
                     margin=dict(l=50, r=50, t=100, b=100), autosize=True)
    fig.update_yaxes(automargin='left')
    return fig


def download_exchange_rate():
    current_date = date.today().strftime('%d/%m/%Y')

    url_exchange_rate = f"http://www.cbr.ru/scripts/XML_dynamic.asp?date_req1=01/07/1992&date_req2={current_date}&VAL_NM_RQ=R01235"

    response = requests.get(url_exchange_rate)

    file_path = './data/exchange_rate.xml'
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print('File downloaded successfully')
    else:
        print('Failed to download file')
    return None

