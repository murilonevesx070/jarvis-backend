import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# Pega a chave OPENAI_API_KEY das variáveis de ambiente do Render
# ou usa a chave informada manualmente abaixo
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "SUA_CHAVE_OPENAI_AQUI")

# Inicializa o cliente da OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "online", "message": "JARVIS com OpenAI (ChatGPT) ativo!"})

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json() or {}
        user_message = data.get("message", "")

        if not user_message:
            return jsonify({"response": "Comando não detectado, Mestre Murilo."}), 400

        # Prompt de sistema para definir o tom do JARVIS
        system_instructions = (
            "Você é o JARVIS, a inteligência artificial criada para auxiliar seu Mestre Murilo. "
            "Responda em Português do Brasil de forma inteligente, direta, cortês e levemente bem-humorada."
        )

        # Chamada ao modelo GPT da OpenAI
        completion = client.chat.completions.create(
            model="gpt-4o-mini",  # Modelo rápido, inteligente e econômico
            messages=[
                {"role": "system", "content": system_instructions},
                {"role": "user", "content": user_message}
            ]
        )

        resposta = completion.choices[0].message.content
        return jsonify({"response": resposta})

    except Exception as e:
        print(f"Erro na requisição OpenAI: {e}")
        return jsonify({"response": f"Desculpe, Mestre Murilo. Falha ao conectar à rede neural: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
