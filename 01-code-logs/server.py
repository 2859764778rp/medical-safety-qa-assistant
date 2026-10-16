from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)
client = OpenAI(base_url="http://127.0.0.1:22222/v1", api_key="EMPTY")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    if isinstance(data, str):
        data = {"prompt": data}
    print("收到请求:", data, flush=True)
    messages = data.get("messages")
    if messages is None:
        prompt = (data.get("prompt") or data.get("question")
                  or data.get("query") or data.get("content")
                  or data.get("text") or data.get("input")
                  or data.get("message") or data.get("user") or "")
        messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model="qwen2.5-7b-medical",
        messages=messages,
        max_tokens=512
    )
    return jsonify({"response": response.choices[0].message.content})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=20003, threaded=True)
