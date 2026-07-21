import os
import wikipedia
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Configura a Wikipédia para Português
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

        msg_clean = user_message.lower()

        # 1. TRATAMENTO DE SAUDAÇÕES
        saudacoes = ["ola", "olá", "oi", "jarvis", "bom dia", "boa tarde", "boa noite", "fala jarvis"]
        if any(s in msg_clean for s in saudacoes) and len(msg_clean.split()) <= 4:
            resposta_texto = "Olá, Mestre Murilo! Sistema Prism OS online e totalmente operacional. Em que posso ajudar?"

        # 2. PESQUISA INTELIGENTE (Busca os títulos relevantes primeiro)
        else:
            try:
                # Pesquisa os artigos relacionados na Wikipédia
                busca = wikipedia.search(user_message)
                
                if busca:
                    # Pega o primeiro artigo encontrado
                    top_resultado = busca[0]
                    resumo = wikipedia.summary(top_resultado, sentences=2)
                    resposta_texto = f"Mestre Murilo, segundo minhas pesquisas sobre '{top_resultado}': {resumo}"
                else:
                    resposta_texto = f"Mestre Murilo, não encontrei informações sobre '{user_message}' no momento."

            except Exception as e:
                print(f"Erro na Wikipédia: {e}")
                resposta_texto = f"Desculpe, Mestre Murilo. Não consegui resgatar essa informação na Wikipédia agora."

        return jsonify({
            "response": resposta_texto,
            "resposta": resposta_texto
        })

    except Exception as e:
        print(f"Erro no servidor: {e}")
        erro_msg = f"Desculpe, Mestre Murilo. Falha de processamento: {str(e)}"
        return jsonify({"response": erro_msg, "resposta": erro_msg}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
