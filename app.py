import os
import wikipedia
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Configura a Wikipédia para Português do Brasil
wikipedia.set_lang("pt")

@app.route('/', methods=['GET'])
@app.route('/get_status', methods=['GET', 'OPTIONS'])
def home():
    if request.method == 'OPTIONS':
        return '', 200
    return jsonify({
        "status": "online",
        "service": "JARVIS Web Core",
        "message": "JARVIS Web totalmente operacional!"
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

        msg_lower = user_message.lower()

        # Respostas rápidas e diretas do JARVIS
        if any(g in msg_lower for g in ["ola", "olá", "oi", "jarvis", "bom dia", "boa tarde", "boa noite"]):
            if len(msg_lower.split()) <= 3:
                resposta_texto = "Olá, Mestre Murilo! Sistema online e pronto para servir. Em que posso ajudar hoje?"
            else:
                resposta_texto = None
        else:
            resposta_texto = None

        # Se não for só uma saudação, busca na Wikipédia / Web
        if not resposta_texto:
            try:
                # Busca o resumo do assunto na Wikipédia
                resumo = wikipedia.summary(user_message, sentences=2)
                resposta_texto = f"Mestre Murilo, segundo as minhas buscas: {resumo}"
            except wikipedia.exceptions.DisambiguationError as e:
                # Se o termo tiver vários significados, pega a primeira opção
                try:
                    resumo = wikipedia.summary(e.options[0], sentences=2)
                    resposta_texto = f"Mestre Murilo, encontrei isto: {resumo}"
                except Exception:
                    resposta_texto = f"Mestre Murilo, o termo '{user_message}' possui vários significados. Pode ser mais específico?"
            except wikipedia.exceptions.PageError:
                resposta_texto = f"Desculpe, Mestre Murilo. Não encontrei uma página direta sobre '{user_message}', mas o sistema continua online!"
            except Exception as e:
                resposta_texto = f"Mestre Murilo, tive um pequeno solavanco na busca, mas estou operacional!"

        return jsonify({
            "response": resposta_texto,
            "resposta": resposta_texto
        })

    except Exception as e:
        print(f"Erro no processamento: {e}")
        erro_msg = f"Desculpe, Mestre Murilo. Ocorreu um erro no servidor: {str(e)}"
        return jsonify({"response": erro_msg, "resposta": erro_msg}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
