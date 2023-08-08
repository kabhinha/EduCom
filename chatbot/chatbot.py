from flask import Flask, request, render_template, jsonify
from chat import getresponse

app = Flask(__name__)

@app.get("/")
def index_get():
    return render_template("chatbot.html")

@app.post("/predict")
def pridict():
    text = request.get_json().get("message")
    response = getresponse(text)
    message = {"answer": response}
    return jsonify(message)

if __name__ == "__main__":
    app.run(debug=True)