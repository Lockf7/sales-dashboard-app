from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    chart_html = ""
    table_html = ""
    if request.method == "POST":
        file = request.files["file"]
        if file.filename.endswith(".csv"):
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(file.filename))
            file.save(filepath)
            df = pd.read_csv(filepath)
            fig = px.bar(df, x="Date", y="Revenue", title="Sales Revenue by Date")
            chart_html = fig.to_html(full_html=False)
            table_html = df.to_html(classes="table table-striped", index=False)
    return render_template("index.html", chart_html=chart_html, table_html=table_html)

if __name__ == "__main__":
    app.run(debug=True)
