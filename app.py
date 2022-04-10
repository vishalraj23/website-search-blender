from flask import Flask, render_template, request, flash

app = Flask(__name__)
app.secret_key = "password"


@app.route("/hello")
def index():
    flash("Click to play video")
    return render_template("index.html")


@app.route("/greet", methods=['POST', 'GET'])
def greeter():
    flash("Hi " + str(request.form['name_input']) + ", great to see you!")
    return render_template("index.html")
