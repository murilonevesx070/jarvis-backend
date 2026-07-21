import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
# Libera o CORS para qualquer requisição do Lovable
CORS(app, resources={r"/*": {"origins": "*"}})

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

# TRATA A ROTA QUE DEU ERRO 404 NO SEU LOG:
@app.route('/', methods=['GET'])
@app.route('/get_status', methods=['GET', 'OPTIONS'])
def home():
    if request.method == 'OPTIONS':
        return '', 200
    return jsonify({
        "status": "online",
        "service": "JARVIS OpenAI Core",
        "message": "JARVIS ativo!"
    })

# TRATA AS ROTAS DE PERGUNTA/CHAT:
@app.route('/chat', methods=['POST', 'OPTIONS'])
@app.route('/pergunta', methods=['POST', 'OPTIONS'])
def chat():
    if request.method == 'OPTIONS':
        return '', 200

    try:
        data = request.get_json(silent=True) or {}
        user_message = data.get("message") or data.get("pergunta") or data.get("comando") or ""

        if not user_message:
            return jsonify({"response": "Comando não detectado, Mestre Murilo.", "resposta": "Comando não detectado, Mestre Murilo."}), 400

        if not client:
            msg_erro = "Erro: OPENAI_API_KEY não foi configurada no Render."
            return jsonify({"response": msg_erro, "resposta": msg_erro}), 500

        system_instructions = (
            "Você é o JARVIS, assistente virtual ultra-inteligente do Mestre Murilo. "
            "Responda em Português do Brasil com um tom elegante, direto e prestativo."
        )

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_instructions},
                {"role": "user", "content": user_message}
            ]
        )

        resposta_texto = completion.choices[0].message.content

        return jsonify({
            "response": resposta_texto,
            "resposta": resposta_texto
        })

    except Exception as e:
        print(f"Erro na requisição OpenAI: {e}")
        erro_msg = f"Desculpe, Mestre Murilo. Falha no processamento: {str(e)}"
        return jsonify({"response": erro_msg, "resposta": erro_msg}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
