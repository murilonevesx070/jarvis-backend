import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
from google.genai import types

app = Flask(__name__)
CORS(app)

# Cole sua API key entre as aspas abaixo OU configure como variável de ambiente no Render
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "SUA_CHAVE_API_AQUI")

client = genai.Client(api_key=GEMINI_API_KEY)

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "online",
        "service": "JARVIS AI Core",
        "message": "Sistema JARVIS totalmente operacional e conectado à rede!"
    })

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json() or {}
        user_message = data.get("message", "")

        if not user_message:
            return jsonify({"response": "Comando não detectado, Mestre Murilo."}), 400

        prompt_sistema = (
            "Você é o JARVIS, a inteligência artificial ultra-avançada criada para auxiliar "
            "seu Mestre Murilo. Responda em Português do Brasil (pt-BR) com um tom elegante, "
            "prestativo, inteligente e levemente irônico quando apropriado. "
            "Você tem acesso à pesquisa na web em tempo real e deve usar informações atualizadas "
            "para responder a qualquer pergunta do Mestre Murilo de forma clara e objetiva."
        )

        full_prompt = f"{prompt_sistema}\n\n[Mestre Murilo]: {user_message}\n[JARVIS]:"

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=full_prompt,
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())]  # Ativa busca na internet
            )
        )

        resposta_texto = response.text if response.text else "Processamento concluído, Mestre. Sem resposta adicional."

        return jsonify({"response": resposta_texto})

    except Exception as e:
        print(f"Erro ao processar comando: {e}")
        return jsonify({
            "response": f"Desculpe, Mestre Murilo. Ocorreu uma falha na minha rede neural ao processar o comando. (Detalhes: {str(e)})"
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
