import pandas as pd
import numpy as np
import joblib
import os
from pickle import dump, load



class HimalXGB():

    def predict_model(self, data):
        """
        This function takes a DataFrame and returns an array with the predictions'score
        """

        df = data.copy()

        # load the pipeline & the model
        model = joblib.load('assets/XGB_model.joblib')
        print(model)
        pipe = joblib.load("assets/pipe_transformation.joblib")
        print(pipe)

        X = pipe.transform(df)
        print(X)

        a = model.predict_proba(X)
        b = model.predict(X)
        res = np.insert(a,2,b, axis=1)

        return res
