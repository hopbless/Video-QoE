import numpy as np
import flask
from flask import Flask, render_template, request, redirect
from measurement import run_video
import pandas as pd
from sklearn.preprocessing import StandardScaler
import pickle as pk




app = Flask(__name__, template_folder='templates')

hope =""
qoeResult =0

@app.route("/", methods=["GET","POST"])
def home():
    if flask.request == "POST":
        result = "Hope"
        qoeResult = predictQoE()
        print("Result", qoeResult)
    else:
        result =""
        qoeResult=0
    return render_template("index.html", hope=result, qoe= qoeResult )




@app.route("/automation", methods= ['GET', 'POST'])
def play():
    return render_template("video_player.html")


@app.route("/measurement", methods =["GET", "POST"])
def record_data():
    run_video()
    return render_template("about.html")

@app.route("/about", methods =["POST", "GET"])
def about_page():
    render_template("about.html", hope = "Result")


def predictQoE():

    with open('svr_model.pkl','rb') as file:
        svr_model = pk.load(file)

    df = pd.read_csv("data/streams.csv", header=0)
    df.head()
    X = df.loc[:, df.columns != "score"]
    type(X)
    y = df["score"]
    type(y)
    scaler = StandardScaler()
    x_std = scaler.fit_transform(X)
    qoeResult = svr_model.predict(x_std)

    return qoeResult





if __name__ == "__main__":
    app.run()
