import os
import wikipedia
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Define a pesquisa da Wikipédia em Português
wikipedia.set_lang("pt")

@app.route('/', methods=['GET'])
@app.route('/get_status', methods=['GET', 'OPTIONS'])
def home():
    if request.method == 'OPTIONS':
        return '', 200
    return jsonify({
        "status": "online",
        "service": "JARVIS Web Core",
        "message": "JARVIS operacional!"
    })

@app.route('/chat', methods=['POST', 'OPTIONS'])
@app.route('/pergunta', methods=['POST', 'OPTIONS'])
def chat():
    if request.method == 'OPTIONS':
        return '', 200

    try:
        data = request.get_json(silent=True) or {}
        user_message = (data.get("message") or data.get("pergunta") or data.get("comando") or "").strip()

        if not user_message:
            return jsonify({
                "response": "Comando não detectado, Mestre Murilo.",
                "resposta": "Comando não detectado, Mestre Murilo."
            }), 400

        # Normaliza o texto (tudo em minúsculas e sem espaços extras)
        msg_clean = user_message.lower()

        # Lista de saudações comuns
        saudacoes = ["ola", "olá", "oi", "jarvis", "bom dia", "boa tarde", "boa noite", "fala jarvis", "hey jarvis"]

        # 1. SE FOR UMA SAUDAÇÃO (Responde direto sem buscar na web)
        if any(s in msg_clean for s in saudacoes) and len(msg_clean.split()) <= 4:
            resposta_texto = "Olá, Mestre Murilo! Sistema Prism OS online e totalmente operacional. Em que posso ajudar hoje?"

        # 2. SE FOR UMA PERGUNTA OU CONCEITO (Busca na Wikipédia em PT)
        else:
            try:
                # Tenta buscar o resumo de 2 frases
                resumo = wikipedia.summary(user_message, sentences=2)
                resposta_texto = f"Mestre Murilo, segundo minhas pesquisas: {resumo}"
            except wikipedia.exceptions.DisambiguationError as e:
                # Caso o termo tenha múltiplos significados, pega a primeira opção válida
                try:
                    resumo = wikipedia.summary
