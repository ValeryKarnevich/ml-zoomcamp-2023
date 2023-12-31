import numpy as np
from io import BytesIO
from urllib import request
from PIL import Image
import tflite_runtime.interpreter as tflite


interpreter = tflite.Interpreter(model_path='bees-wasps-v2.tflite')
interpreter.allocate_tensors()

input_index = interpreter.get_input_details()[0]['index']
output_index = interpreter.get_output_details()[0]['index']


def download_image(url):
    with request.urlopen(url) as resp:
        buffer = resp.read()
    stream = BytesIO(buffer)
    img = Image.open(stream)
    return img


def prepare_image(img, target_size):
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img = img.resize(target_size, Image.NEAREST)
    return img


def preprocess_input(img_resized):
    x = np.array(img_resized, dtype='float32')
    X = np.array([x])
    X /= 255
    return X


def predict(url):
    img = download_image(url)
    img_resized = prepare_image(img, (150, 150))
    X = preprocess_input(img_resized)

    interpreter.set_tensor(input_index, X)
    interpreter.invoke()
    pred = interpreter.get_tensor(output_index)
    float_prediction = pred[0].tolist()

    return float_prediction


def lambda_handler(event, context):
    url = event['url']
    result = predict(url)
    return result