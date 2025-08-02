import tensorflow as tf 
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd
import requests
from fastapi import FastAPI
import os

DATA_DIR='./data/energy.csv'
app=FastAPI()

if not os.path.exists(DATA_DIR):
    raise FileNotFoundError(f"Data file not found at {DATA_DIR}")
else:
    print('file path exists')

data=pd.read_csv(DATA_DIR)


# Assuming that all the columns are features except the last one 

X=data.iloc[:,:-1]
Y=data.iloc[:,-1]

print(f"your features data is {X}")
print(f"your target data is {Y}")

x_train, x_test, y_train, y_test= train_test_split(X, Y, test_size=0.2,random_state=42)

scaler=StandardScaler()
x_train=scaler.fit_transform(x_train)
x_test=scaler.fit_transform(x_test)

model=keras.Sequential(
    [ keras.layers.Dense(64,activation='relu',input_shape=(x_train.shape[1],)),
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dense(1)
    ]
)

try:
    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])
    model.fit(x_train,y_train,epochs=50,batch_size=32,validation_split=0.1)

    loss, mae=model.evaluate(x_test,y_test)
    print(f"Test MAE {mae}")
    model.save("energy_model.h5")
    import joblib 

    joblib.dump(scaler,'scaler.save')
    print(f"your model as of mow is {model.summary()}")
except Exception as e:
    print(f"error occured during the training and saving {e}")
