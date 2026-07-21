import os
import wikipedia
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Define a pesquisa para o Português
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

        # 1. TRATAMENTO DE SAUDAÇÕES (Não pesquisa na internet)
        saudacoes = ["ola", "olá", "oi", "jarvis", "bom dia", "boa tarde", "boa noite", "fala jarvis"]
        
        # Se for uma mensagem curta e contiver uma saudação
        if any(s in msg_clean for s in saudacoes) and len(msg_clean.split()) <= 4:
            resposta_texto = "Olá, Mestre Murilo! Sistema Prism OS online e totalmente operacional. Como posso ajudar?"
        
        # 2. SE FOR UMA PERGUNTA / PESQUISA REAL
        else:
            try:
                # Busca resumo de 2 frases na Wikipédia
                resumo = wikipedia.summary(user_message, sentences=2)
                resposta_texto = f"Mestre Murilo, segundo minhas buscas: {resumo}"
            except wikipedia.exceptions.DisambiguationError as e:
                # Caso haja múltiplos significados
                try:
                    resumo = wikipedia.summary(e.options[0], sentences=2)
                    resposta_texto = f"Mestre Murilo, encontrei o seguinte: {resumo}"
                except Exception:
                    resposta_texto = f"Mestre Murilo, o termo '{user_message}' possui vários significados. Pode detalhar melhor?"
            except wikipedia.exceptions.PageError:
                resposta_texto = f"Mestre Murilo, não encontrei registros diretos sobre '{user_message}', mas continuo a postos."
            except Exception:
                resposta_texto = f"Desculpe, Mestre Murilo. Ocorreu uma instabilidade na consulta, mas o sistema está ativo."

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
