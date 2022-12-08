from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
app = Flask(__name__)
import numpy as np
import pandas as pd


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
CLASS_NAMES = ['Bean',
 'Bitter_Gourd',
 'Bottle_Gourd',
 'Brinjal',
 'Broccoli',
 'Cabbage',
 'Capsicum',
 'Carrot',
 'Cauliflower',
 'Cucumber',
 'Papaya',
 'Potato',
 'Pumpkin',
 'Radish',
 'Tomato']
CORS(app)


@app.route("/")
def hello():
    return "Hello world"


@app.route("/predict",methods=["POST"])
def predict():
    print("I am here")
    try:        
        # body = request.json
        file = request.files['image']
        file.save(file.filename)
        payload = request.form.to_dict()
        print(payload,file)
        modelParam = payload['modelParam']
        if modelParam == "VGG16":
            model = Vgg16_model
        elif modelParam == "ResNet":
            model = Resnet_model
        elif modelParam == "MobileNet":
            model = MobileNet
        print("Model selected")
        image  = tf.keras.utils.load_img("/home/chowtagowtham/veg-classification/backend/"+file.filename)
        image = image.resize((224,224))
        img = np.array(image)
        img = img* 1.0/255
        
        print("Image loaded")
        img = np.expand_dims(img,0)
        y_pred = model.predict(img)
        print(y_pred[0],y_pred[0].shape)
        print(y_pred.shape)
        print(np.argsort(y_pred[0]))
        top3PredictedIndexes = np.argsort(y_pred[0])[::-1][:3]
        top3PredictedClasses = []
        top3PredictedPropbabilities = []
        for out in top3PredictedIndexes:
            top3PredictedClasses.append(str(CLASS_NAMES[out]))
            top3PredictedPropbabilities.append(str(y_pred[0][out]))                                
        out = {"CLASS_NAMES":CLASS_NAMES[np.argmax(y_pred)], "classes": top3PredictedClasses, "prob": top3PredictedPropbabilities}
        print(out)
        return out

    except Exception as e:
        print(e)
        return "False"



if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5001)