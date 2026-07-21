import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from duckduckgo_search import DDGS

app = Flask(__name__)
# Libera o acesso para o Lovable não ser bloqueado
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/', methods=['GET'])
@app.route('/get_status', methods=['GET', 'OPTIONS'])
def home():
    if request.method == 'OPTIONS':
        return '', 200
    return jsonify({
        "status": "online",
        "service": "JARVIS Web Engine",
        "message": "JARVIS Web totalmente operacional!"
    })

@app.route('/chat', methods=['POST', 'OPTIONS'])
@app.route('/pergunta', methods=['POST', 'OPTIONS'])
def chat():
    if request.method == 'OPTIONS':
        return '', 200

    try:
        data = request.get_json(silent=True) or {}
        user_message = data.get("message") or data.get("pergunta") or data.get("comando") or ""

        if not user_message:
            return jsonify({
                "response": "Comando não detectado, Mestre Murilo.",
                "resposta": "Comando não detectado, Mestre Murilo."
            }), 400

        # Tenta usar a IA nativa da Web via DuckDuckGo (Grátis e sem chave)
        resposta_texto = ""
        try:
            with DDGS() as ddgs:
                # Usa a IA da Web sem precisar de chave ou login
                resposta_ddg = ddgs.chat(user_message, model='gpt-4o-mini')
                if resposta_ddg:
                    resposta_texto = resposta_ddg
        except Exception:
            resposta_texto = ""

        # Se falhar a IA da Web, busca os resultados direto na pesquisa da internet
        if not resposta_texto:
            with DDGS() as ddgs:
                results = list(ddgs.text(user_message, region='br-pt', max_results=3))
            
            if results:
                resposta_texto = f"Mestre Murilo, encontrei as seguintes informações na internet:\n\n"
                for item in results:
                    resposta_texto += f"• {item['body']}\n\n"
            else:
                resposta_texto = f"Mestre Murilo, não consegui encontrar informações sobre esse assunto na internet no momento."

        return jsonify({
            "response": resposta_texto,
            "resposta": resposta_texto
        })

    except Exception as e:
        print(f"Erro no processamento Web: {e}")
        erro_msg = f"Desculpe, Mestre Murilo. Falha ao acessar a internet: {str(e)}"
        return jsonify({"response": erro_msg, "resposta": erro_msg}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
