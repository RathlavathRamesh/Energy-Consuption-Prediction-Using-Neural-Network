
import tensorflow as tf
import pandas as pd 
from fastapi import FastAPI 
from pydantic import BaseModel
import joblib
import numpy as np

app=FastAPI()


model=tf.keras.models.load_model('./energy_model.h5') 
scaler=joblib.load('./scaler.save') 

class Features(BaseModel):
    data:list

@app.post('/predict')
def predict(features:Features):
    try:
        X=np.array(features.data).reshape(1,-1)
        x_scaled=scaler.transform(X) 
        prediction=model.predict(x_scaled)[0][0] 
        print(f"your prediction is {prediction}") 
        return f"Energy consumption for the given input data is {prediction} Units"
    except Exception as e:
        print(f"Error occured during the model testing{e}")

