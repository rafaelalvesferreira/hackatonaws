#!/usr/bin/env python3
"""
API Flask Simples - Garantida para funcionar
"""

from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'message': 'API Flask simples funcionando',
        'port': 5002
    })

@app.route('/test')
def test():
    return jsonify({
        'message': 'Teste bem-sucedido!',
        'working': True
    })

if __name__ == '__main__':
    print("🚀 Iniciando API Flask Simples...")
    print("🌐 Disponível em: http://localhost:5002")
    print("📋 Endpoints: /health, /test")
    print("⏹️  Pressione Ctrl+C para parar")
    
    app.run(
        host='0.0.0.0',
        port=5002,
        debug=False
    )
