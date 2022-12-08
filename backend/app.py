from flask import Flask, request, make_response
from flask_cors import CORS
app = Flask(__name__)
import os
import glob
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Tensorflow import
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.layers import Conv2D, MaxPooling2D, GlobalAveragePooling2D, Dense, ReLU, Softmax, BatchNormalization, Dropout
from tensorflow.random import set_seed
from tensorflow import keras
BASEPATH="/home/chowtagowtham/Modelsmall"
Vgg16_model = keras.models.load_model(f'{BASEPATH}/my_h5_VGG16_model.h5')
Resnet_model =  keras.models.load_model(f'{BASEPATH}/my_h5_Resnet_model.h5')
MobileNet =  keras.models.load_model(f'{BASEPATH}/my_h5_mobilenet_model.h5')

CORS(app)


@app.route("/")
def hello():
    return "Hello world"


@app.route("/predict",methods=["POST"])
def predict():
    body = request.get_json()
    print(body)
    img = body['img']
    modelParam = body['modelParam']
    if modelParam == "VGG16":
        model = Vgg16_model
    elif modelParam == "ResNet":
        model = Resnet_model
    elif modelParam == "MobileNet":
        model = MobileNet
    
    # img = np.array(tf.keras.utils.load_img(img))
    # img = np.expand_dims(img,0)
    # y_pred = model.predict(img)
    # return y_pred
    return "True"



if __name__ == '__main__':
    app.run(host="0.0.0.0")