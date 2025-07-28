from flask import Flask, request, jsonify
from flask_cors import CORS
from ai import get_ai_response  # Your AI response function

app = Flask(__name__)
CORS(app)

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data['question']
    answers = get_ai_response(question)
    full_answer = " ".join(answers)
    return jsonify({'answer': full_answer})

if __name__ == '__main__':
    app.run(debug=True)
