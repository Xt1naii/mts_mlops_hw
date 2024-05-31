import pandas as pd


class ClfModel:
    def __init__(self, model, threshold):
        self.model = model
        self.threshold = threshold

    def predict(self, input_df: pd.DataFrame):
        probas = self.model.predict_proba(input_df)[:, 1]
        return (probas >= self.threshold).astype(int)
    
    def predict_proba(self, input_df: pd.DataFrame):
        probas = self.model.predict_proba(input_df)[:, 1]
        return probas
