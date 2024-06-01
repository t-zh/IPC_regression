
import json
from flask import Flask
from flask import render_template
import plotly
# import pickle
from utils import download_file, plot_the_graph, download_exchange_rate
from models import preproc, base_model

app = Flask(__name__)
#Download data containing the Consumer price index from https://rosstat.gov.ru
download_file()
download_exchange_rate()
#Data prepocessing
df = preproc.prepocessing_data('./data/ipc_mes.xlsx')
#Add exchange rate data
df_augumented = preproc.augument_data_by_exchange_rate(df)
#Loading models
model = base_model.train_model(df_augumented)
# pickle.dump(model, open('model.pkl', 'wb'))

@app.route('/')
def show_plotly():

    X_pred = preproc.prepare_data_for_prediction(df)
    X_pred['exchange_rate'] = df_augumented['exchange_rate'].iloc[-1]
    predictions = model.predict(X_pred)

    X, y = preproc.prepare_data_for_plotting(df, X_pred, predictions, period_in_months=100)
    # Create a Plotly graph
    fig = plot_the_graph(X, y)
    # Convert the figure to JSON
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('graph.html', graphJSON=graphJSON)

if __name__ == '__main__':
    app.run(debug=False)
