
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor

def train_model(df):
    X = df[['month', 'year', 'exchange_rate']]
    y = df['ipc']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = GradientBoostingRegressor(random_state=42)
    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)
    print(f"R2_Score: {score}")
    # pickle.dump(model, open('model.pkl', 'wb'))
    return model
