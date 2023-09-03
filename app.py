from flask import Flask, render_template, request, jsonify
import zhipuai

zhipuai.api_key = "YOUR-API-KEY-HERE"

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('user_input')
    response = zhipuai.model_api.sse_invoke(
        model="chatglm_pro",
        prompt=[{"role": "user", "content": user_input}],
        temperature=0.9,
        top_p=0.7,
        incremental=True
    )

    chat_response = ""
    for event in response.events():
        if event.event == "add":
            chat_response += event.data
        elif event.event == "error" or event.event == "interrupted":
            chat_response += event.data
        elif event.event == "finish":
            chat_response += event.data
    return jsonify({"response": chat_response})

if __name__ == '__main__':
    app.run(debug=True)
