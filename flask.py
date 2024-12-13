from flask import Flask, render_template, request
import librosa
import numpy as np
from tensorflow.keras.models import load_model

app = Flask(__name__)

def extract_features(file_name):
    audio, sample_rate = librosa.load(file_name, res_type='kaiser_fast')
    if audio.size < 88160:
        d = np.pad(audio, (88160 - audio.size, 0), mode='constant')
    else:
        d = audio[0:88160]

    mfccs = librosa.feature.mfcc(y=d, sr=sample_rate, n_mfcc=128)
    return mfccs

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/predict", methods=['POST'])
def predict():
    labels_mapping = {0: 'Air_conditioner', 1: 'Car_horn', 2: 'Children_playing', 3: 'Dog_bark',
                  4: 'Drilling', 5: 'Engine_idling', 6: 'Gun_shot', 7: 'Jackhammer', 8: 'Siren', 9: 'Street_music'}

    audio_file = request.files['audio_file']
    data_mfcc = extract_features(audio_file)
    data_mfcc = data_mfcc.reshape(1, 128, 173, 1)
    model = load_model('weights.best.basic_cnn_mfcc1.hdf5')
    predicted_class = (model.predict_classes(data_mfcc))
    return render_template("prediction.html", label = (labels_mapping[predicted_class[0]]))


if __name__ == "__main__":
    app.run(debug=False)
