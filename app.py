from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)  # enable access from browser

client = OpenAI(
    base_url="https://api.aimlapi.com/v1",
    api_key="0710951b319a4cd79e155a8e40413658",  # no "Bearer"
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "")

    if not user_input:
        return jsonify({"reply": "Please enter a message."}), 400

    try:
        response = client.chat.completions.create(
            model="google/gemma-3n-e4b-it",
            messages=[{"role": "user", "content": user_input +""}],
            temperature=0.7,
            top_p=0.7,
            frequency_penalty=1,
        )
        reply = response.choices[0].message.content
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
