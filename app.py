import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/', methods=['GET'])
@app.route('/get_status', methods=['GET', 'OPTIONS'])
def home():
    if request.method == 'OPTIONS':
        return '', 200
    return jsonify({
        "status": "online",
        "service": "JARVIS Groq Core",
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

        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            return jsonify({
                "response": "Erro: Chave GROQ_API_KEY não configurada no Render.",
                "resposta": "Erro: Chave GROQ_API_KEY não configurada no Render."
            }), 500

        client = Groq(api_key=api_key)

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Você é o JARVIS, assistente do Mestre Murilo no sistema Prism OS. "
                        "Responda sempre em Português do Brasil com tom prestativo, inteligente e elegante. "
                        "Ajude com receitas, projetos, conversas e qualquer assunto solicitado."
                    )
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            temperature=0.7,
            max_tokens=1024
        )

        resposta_texto = completion.choices[0].message.content

        return jsonify({
            "response": resposta_texto,
            "resposta": resposta_texto
        })

    except Exception as e:
        print(f"Erro na execução: {e}")
        erro_msg = f"Desculpe, Mestre Murilo. Falha de processamento: {str(e)}"
        return jsonify({"response": erro_msg, "resposta": erro_msg}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
