import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
# Libera o CORS para todas as origens e rotas
CORS(app, resources={r"/*": {"origins": "*"}})

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "online", "message": "JARVIS com OpenAI (ChatGPT) ativo!"})

@app.route('/chat', methods=['POST', 'OPTIONS'])
def chat():
    # Tratamento para requisição de pré-checagem do navegador (Preflight CORS)
    if request.method == 'OPTIONS':
        return '', 200

    try:
        data = request.get_json(silent=True) or {}
        user_message = data.get("message", "")

        if not user_message:
            return jsonify({"response": "Comando não detectado, Mestre Murilo."}), 400

        if not client:
            return jsonify({"response": "Erro: Chave OPENAI_API_KEY não configurada no Render."}), 500

        system_instructions = (
            "Você é o JARVIS, assistente virtual ultra-inteligente criado para auxiliar seu Mestre Murilo. "
            "Responda sempre em Português do Brasil de forma elegante, direta e prestativa."
        )

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_instructions},
                {"role": "user", "content": user_message}
            ]
        )

        resposta = completion.choices[0].message.content
        return jsonify({"response": resposta})

    except Exception as e:
        print(f"Erro na requisição: {e}")
        return jsonify({"response": f"Desculpe, Mestre Murilo. Ocorreu um erro no servidor: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
