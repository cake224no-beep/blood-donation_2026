from flask import Flask, request, redirect
import json
from datetime import datetime
from zoneinfo import ZoneInfo

app = Flask(__name__)

DATA_FILE = "queue.json"

def read_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

@app.route("/")
def home():

    data = read_data()

    return f"""
    <html>
    <head>
        <meta charset="utf-8">
        <meta http-equiv="refresh" content="10">
    </head>

    <body style="
        font-family:Arial;
        text-align:center;
        margin-top:60px;
        background-color:#f8f9fa;
    ">

        <h1>🩸12/18系微捐血活動叫號</h1>

        <h2>目前叫號</h2>

        <div style="
            font-size:80px;
            color:red;
            font-weight:bold;
            margin:30px;
        ">
            {data['currentNo']}
        </div>

        <div style="
            color:gray;
            font-size:20px;
        ">
            最後更新時間：{data['updateTime']}
        </div>

    </body>
    </html>
    """


@app.route("/admin")
def admin():

    data = read_data()

    return f"""
    <html>
    <head>
        <meta charset="utf-8">
    </head>

    <body style="
        font-family:Arial;
        padding:30px;
    ">

        <h1>捐血活動管理頁面</h1>

        <h2>目前叫號：{data['currentNo']}</h2>

        <h3>最後更新：{data['updateTime']}</h3>

        <form action="/update" method="post">
            <input
                type="text"
                name="number"
                value="{data['currentNo']}"
                style="font-size:24px;width:200px;"
            >

            <button
                type="submit"
                style="font-size:24px;"
            >
                更新
            </button>
        </form>

    </body>
    </html>
    """


@app.route("/update", methods=["POST"])
def update():

    data = read_data()

    data["currentNo"] = request.form["number"]

    data["updateTime"] = datetime.now(
        ZoneInfo("Asia/Taipei")
    ).strftime("%H:%M")

    save_data(data)

    return redirect("/admin")


if __name__ == "__main__":
    app.run(debug=True)
