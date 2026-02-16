import pandas as pd
from sklearn.ensemble import IsolationForest

def run_ai_detection(data):

    features = data[
        [
            'login_hour',
            'files_accessed',
            'files_downloaded',
            'failed_logins'
        ]
    ]

    model = IsolationForest(contamination=0.3, random_state=42)

    data['anomaly'] = model.fit_predict(features)

    return data
