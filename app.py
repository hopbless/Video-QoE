import numpy as np
import flask
from flask import Flask, render_template, request, redirect
from measurement import run_video
import pandas as pd
from sklearn.preprocessing import StandardScaler




app = Flask(__name__, template_folder='templates')


@app.route("/", methods=["GET","POST"])
def home():
    result = "Hope"

    return render_template("index.html", hope=result)




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
    
    df = pd.read_csv("data/training_data.csv", header=0)
    X = df.loc[:, df.columns != "score"]
    type(X)
    y = df["score"]
    type(y)
    scaler = StandardScaler()
    x_std = scaler.fit_transform(X)
    y_pred = svr_model.predict(X_train)




if __name__ == "__main__":
    app.run()
