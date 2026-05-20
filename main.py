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
