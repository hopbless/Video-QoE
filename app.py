import numpy as np
import flask
from flask import Flask, render_template, request, redirect
from measurement import run_video
import pandas as pd
from sklearn.preprocessing import StandardScaler
import pickle as pk




app = Flask(__name__, template_folder='templates')

# result =""
# qoeResult =0

@app.route("/")
def home():

    return render_template("index.html")




@app.route("/automation", methods= ['GET', 'POST'])
def play():
    return render_template("video_player.html")

@app.route("/youtube-player", methods= ['GET', 'POST'])
def youTubePlayer():
    return render_template("youtube_page.html")


@app.route("/measurement", methods =["GET", "POST"])
def record_data():
    run_video()
    return render_template("about.html")


@app.route("/predict", methods =["POST"])
def predict():
    global user_mos
    user_mos = request.form.get("mos")
    global qoeResult
    qoeResult = predictQoE()
    print("prediction", qoeResult, user_mos)

    return redirect('/result', qoeResult)


@app.route("/result")
def result():
    return render_template("predict_page.html", qoe=qoeResult, hope=user_mos)



def predictQoE():

    with open('svr_model.pkl','rb') as file:
        svr_model = pk.load(file)

    df = pd.read_csv("data/streams.csv", header=0)
   
    X = df.loc[:, df.columns != "Unnamed: 0"]
    type(X)

    scaler = StandardScaler()
    x_std = scaler.fit_transform(X)
    qoeResult = svr_model.predict(x_std)
    qoeResult = np.round(qoeResult, 2)
    qoe_result = str(qoeResult)

    return qoe_result





if __name__ == "__main__":
    app.run()
