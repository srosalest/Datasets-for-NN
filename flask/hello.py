import os
import base64
import time
from flask import Flask, request, jsonify, render_template
from procedures import *

global model_for_preprocess
global model_for_waste_classification
global model_for_trashnet
global model_for_brand_recognition
global model_for_clothes_recognition

app = Flask(__name__)
model_waste_classification = 'trained-models/From_scratch_V1.json'
model_waste_classification_weight = 'trained-models/From_scratchV1.hdf5'

model_trashnet = 'trained-models/Thrasnet-InceptionResNetV2_adadelta.json'
model_trashnet_weight = 'trained-models/weights_Thrasnet-InceptionResNetV2_adadelta.hdf5'

model_brand_recognition = 'empty'
model_brand_recognition_weight = 'empty'

model_clothes_recognition = 'trained-models/mnist_fashion_adagrad_cnn.json'
model_clothes_recognition_weight = 'trained-models/weights_mnist_fashion_adagrad_cnn.hdf5'


#load models
model_for_preprocess, model_for_waste_classification, model_for_trashnet, model_for_clothes_recognition = load_models(model_waste_classification, 
    model_waste_classification_weight, model_trashnet, model_trashnet_weight, model_brand_recognition,model_brand_recognition_weight, model_clothes_recognition, 
    model_clothes_recognition_weight)

print('model loaded')

@app.route('/', methods=['POST'])
def neural_prediction():
    message = request.get_json(force=True)
    encoded = message['image']
    decoded = base64.b64decode(encoded)
    image = Image.open(io.BytesIO(decoded))

    predictions = predict(image,model_for_preprocess, model_for_waste_classification, model_for_trashnet, model_for_clothes_recognition)

    if (len(predictions) != 0):

        response = {
            'waste': predictions[0],
            'trashnet' : predictions[1],
            'brand' : predictions[2],
            'clothes' : predictions[3]
        }

    else:
        response = {
            'waste': 'organic',
            'trashnet' : 'empty',
            'brand' : 'empty',
            'clothes' : 'empty'
        }

    return jsonify(response)
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000) 
    
