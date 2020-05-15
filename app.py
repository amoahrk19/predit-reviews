from keras.models import load_model
import keras.backend as K
import pickle
from keras.preprocessing.sequence import pad_sequences
import numpy as np
import os


from flask import Flask, render_template, session, redirect, url_for, session, jsonify, request
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import TextAreaField
from wtforms import validators


def prediction(model, tokenizer, comment):
    text_enc = tokenizer.texts_to_sequences([comment])
    padded_text = pad_sequences(text_enc, maxlen=60, padding='post')
    return np.argmax(model.predict(padded_text))


def my_metric_1(y_true, y_pred):
    yp = K.cast_to_floatx(K.argmax(y_pred))
    pred_diff = K.abs(y_true - yp)
    return K.mean(K.less_equal(pred_diff,1))


def my_metric_2(y_true, y_pred):
    yp = K.cast_to_floatx(K.argmax(y_pred))
    pred_diff = K.abs(y_true - yp)
    return K.mean(K.less_equal(pred_diff,2))


if os.path.getsize('tokenizer.pickle') > 0:
    with open('tokenizer.pickle', "rb") as f:
        unpickler = pickle.Unpickler(f)
        t = unpickler.load()


dependencies = {
    'my_metric_1': my_metric_1,
    'my_metric_2':my_metric_1
}

model_5 = load_model("model-5.hdf5", custom_objects=dependencies, compile=False)
model_5._make_predict_function()

model_10 = load_model("model-10.hdf5", custom_objects=dependencies, compile=False)
model_10._make_predict_function()


app = Flask(__name__)

app.config['SECRET_KEY'] = 'This is a very secret string'

Bootstrap(app)

class PredictForm(FlaskForm):
    txt = TextAreaField('Enter Comment', [validators.input_required()], id='txt')


@app.route('/', methods=['POST', 'GET'])
def home():
    form = PredictForm()
    return render_template('home.html', form=form)


@app.route('/process', methods=['POST', 'GET'])
def process():
    text = request.form['text']
    r5 = prediction(model_5, t, text)
    r10 = prediction(model_10, t, text)
    return jsonify({'rating5': str(r5),
                    'rating10': str(r10)})




if __name__ == '__main__':
	app.run(host='0.0.0.0')