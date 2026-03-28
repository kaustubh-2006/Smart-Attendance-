from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route("/")
def index():
    try:
        df = pd.read_csv("attendance.csv")
    except:
        df = pd.DataFrame(columns=["Name","Subject","Date","Time","Method"])

    return render_template("index.html", tables=[df.to_html(index=False)])

if __name__ == "__main__":
    app.run(debug=False)
