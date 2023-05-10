import numpy as np
import flask
from flask import Flask, render_template, request, redirect
from measurement import run_video




app = Flask(__name__, template_folder='templates')


@app.route("/")
def home():
    return render_template("index.html")




@app.route("/automation", methods= ['GET', 'POST'])
def play():
    return render_template("video_player.html")

@app.route("/measurement", methods =["GET", "POST"])
def record_data():
    run_video()
    return render_template("about.html")



if __name__ == "__main__":
    app.run()
