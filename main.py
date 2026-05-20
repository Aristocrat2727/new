from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

OPENAI_KEY = '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'
GROQ_KEYS = [ ... ]  # твои 10 ключей
TINYFISH_KEY = 'sk-tinyfish-5JcBOv7i9Kevj5J0EoJ0yZmfIdZeaJlv'

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    provider = data.get('provider', 'groq')
    prompt = data.get('prompt')
    
    if provider == 'openai':
        # OpenAI API
        headers = { 'Authorization': f'Bearer {OPENAI_KEY}', 'Content-Type': 'application/json' }
        body = { 'model': 'gpt-4o', 'messages': [{'role':'user','content':prompt}], 'max_tokens':2048 }
        resp = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=body)
        return jsonify(resp.json())
    
    elif provider == 'tinyfish':
        # TinyFish Search
        url = f'https://api.search.tinyfish.ai?query={prompt}&location=ru&language=ru'
        resp = requests.get(url, headers={ 'X-API-Key': TINYFISH_KEY })
        return jsonify(resp.json())
    
    else: # groq
        # Groq (ротация ключей)
        # ... твой код
        pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
