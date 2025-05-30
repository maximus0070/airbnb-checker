from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def check_airbnb():
    reserved_dates = ["2025.05.31", "2025.06.07", "2025.06.15"]
    return render_template("index.html", dates=reserved_dates)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
