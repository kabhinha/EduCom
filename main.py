from flask import Flask, request, render_template, jsonify
from chat import getresponse
from lang import answer, summary, Summary

summ = "none"
app = Flask(__name__)

@app.get("/")
def index_get():
    Vars = {
        "summ":"none",
        "ans":"none"
    }
    return render_template("index.html", **Vars)

@app.post("/predict")
def pridict():
    text = request.get_json().get("message")
    response = getresponse(text)
    message = {"answer": response}
    return jsonify(message)

@app.post("/sum_pdf")
def sum_pdf():
    if request.method == 'POST':  
        f = request.files['pdf']
        f.save(f.filename)
        summ = summary(f.filename)
        Vars = {
        "summ":summ,
        "ans":"none"
    }
        print(summ)
        return render_template("index.html", **Vars)

@app.post("/ask_pdf")
def ans_pdf():
    if request.method == 'POST':  
        f = request.files['pdf']
        f.save(f.filename)
        que = request.form["que"]
        ans = Summary(f.filename, que)
        Vars = {
        "summ":"none",
        "ans":ans
    }
        return render_template("index.html", **Vars)


if __name__ == "__main__":
    app.run(debug=True)