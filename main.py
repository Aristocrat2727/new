import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

OPENAI_KEY = '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'

@app.route('/ask', methods=['POST', 'OPTIONS'])
def ask():
    if request.method == 'OPTIONS':
        return '', 200
    
    data = request.json
    prompt = data.get('prompt', '')
    
    headers = {
        'Authorization': f'Bearer {OPENAI_KEY}',
        'Content-Type': 'application/json'
    }
    payload = {
        'model': 'gpt-3.5-turbo',
        'messages': [{'role': 'user', 'content': prompt}],
        'max_tokens': 1024,
        'temperature': 0.7
    }
    
    try:
        resp = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=payload, timeout=30)
        return jsonify(resp.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
