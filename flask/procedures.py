import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import base64
import numpy as np
import io
from PIL import Image
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential, load_model
from keras.models import load_model, model_from_json
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array
from flask import request
from flask import jsonify
from flask import Flask
import cv2
from keras.applications.inception_resnet_v2 import InceptionResNetV2
from keras.models import Model

def preprocess_image_trashnet_fashion(image_decoded, target_size_rgb, target_size_bw, targe_size_waste):

    #convert images to RGB and BW
    if image_decoded.mode != "RGB":
        decoded_trashnet = image_decoded.convert("RGB")
        decoded_fashion = image_decoded.convert("RGB")
        decoded_waste = image_decoded.convert("RGB")
    
    else:
        decoded_trashnet = image_decoded
        decoded_fashion = image_decoded
        decoded_waste = image_decoded

    decoded_trashnet = decoded_trashnet.resize(target_size_rgb)
    decoded_waste = decoded_waste.resize(targe_size_waste)

    decoded_fashion = decoded_fashion.convert("L")
    decoded_fashion = decoded_fashion.resize(target_size_bw)

    #transform to array
    image_trashnet = img_to_array(decoded_trashnet)
    image_fashion = img_to_array(decoded_fashion)
    image_waste = img_to_array(decoded_waste)

    image_trashnet = np.expand_dims(image_trashnet,axis=0)
    image_fashion = np.expand_dims(image_fashion,axis=0)
    image_waste = np.expand_dims(image_waste,axis=0)

    #normalize
    image_trashnet = image_trashnet * float(1/255.0)
    image_fashion = image_fashion * float(1/255.0)
    image_waste = image_waste * float(1/255.0)

    image_trashnet = np.asarray(image_trashnet)
    image_trashnet = image_trashnet.reshape(1,299,299,3)

    image_fashion = np.asarray(image_fashion)
    image_fashion = image_fashion.reshape(1,28,28,1)

    image_waste = np.asarray(image_waste)
    image_waste = image_waste.reshape(1,128,128,3)

    #return images
    return image_trashnet, image_fashion, image_waste

def load_json(model_json, model_weight):
    json_file = open(model_json, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights(model_weight)

    return loaded_model

def load_models(model_waste_classification, model_waste_classification_weight,
     model_trashnet, model_trashnet_weight, model_brand_recognition,model_brand_recognition_weight, model_clothes_recognition, model_clothes_recognition_weight):
    
    #load the models
    model_for_preprocess = InceptionResNetV2(weights='imagenet')
    model_for_preprocess = Model(inputs=model_for_preprocess.inputs, outputs=model_for_preprocess.layers[-2].output)

    model_for_waste_classification = load_json(model_waste_classification, model_waste_classification_weight)
    model_for_trashnet = load_json(model_trashnet, model_trashnet_weight)
    model_for_brand_recognition = load_json(model_brand_recognition, model_brand_recognition_weight)
    model_for_clothes_recognition = load_json(model_clothes_recognition, model_clothes_recognition_weight)

    return model_for_preprocess, model_for_waste_classification, model_for_trashnet, model_for_clothes_recognition, model_for_brand_recognition

def prediction_interpretation(prediction_list_values):

    prediction = sorted(range(len(prediction_list_values)), key = lambda sub: prediction_list_values[sub])[-2:]

    if (prediction_list_values[prediction[0]] >= prediction_list_values[prediction[1]]):
        return prediction[0]
    else:
        return prediction[1]


def get_predictions(image_rgb, image_bw, image_waste, model_for_preprocess, model_for_waste_classification, model_for_trashnet, model_for_clothes_recognition, model_for_brand_recognition):

    #waste classification
    classes_waste = ['organic','inorganic']
    prediction_waste_classification = model_for_waste_classification.predict(image_waste)
    prediction_1 =classes_waste[int(np.around(prediction_waste_classification[0], decimals=0)[0])]

    if (prediction_1 != 'organic'):

        #trashnet classification
        classes_trashnet = ['cardboard','glass','metal','paper','plastic','trash']
        preprocess_trashnet = model_for_preprocess(image_rgb)
        prediction_trashnet = model_for_trashnet.predict(preprocess_trashnet).tolist()
        prediction_trashnet = prediction_interpretation(prediction_trashnet[0])
        prediction_2 = classes_trashnet[prediction_trashnet]

        #brand recognition
        classes_brand = ['adidas','aldi','apple','becks','bmw','carlsberg','chimay','cocacola','corona','dhl','erdinger','esso',
            'fedex','ferrari','ford','foster','google','guiness','heineken','hp','milka','no-logo','nvidia','paulaner','pepsi',
            'rittersport','shell','singha','starbucks','stellaartois','texaco','tsingtao','ups']
        prediction_brand_recognition = model_for_brand_recognition.predict(image_waste).tolist() #uses the same 128x128 rgb image from waste
        prediction_brand_recognition = prediction_interpretation(prediction_brand_recognition[0])
        prediction_3 = classes_brand[prediction_brand_recognition]

        #clothes classification
        classes_clothes = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
            'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
        prediction_clothes_recognition = model_for_clothes_recognition.predict(image_bw).tolist()
        prediction_clothes_recognition = prediction_interpretation(prediction_clothes_recognition[0])
        prediction_4 = classes_clothes[prediction_clothes_recognition]

        prediction = [prediction_1, prediction_2, prediction_3 ,prediction_4]

    else:
        prediction = []

    return prediction

def predict(image_decoded,model_for_preprocess, model_for_waste_classification, model_for_trashnet, model_for_clothes_recognition, model_for_brand_recognition):

    target_size_bw =  [28,28]
    target_size_rgb = [299,299]
    targe_size_waste = [128,128]

    image_rgb, image_bw, image_waste = preprocess_image_trashnet_fashion(image_decoded, target_size_rgb, target_size_bw, targe_size_waste)
    predictions = get_predictions(image_rgb, image_bw, image_waste, model_for_preprocess, model_for_waste_classification, model_for_trashnet, model_for_clothes_recognition, model_for_brand_recognition)

    return predictions

if __name__ == "__main__":
    print("Hello-World")