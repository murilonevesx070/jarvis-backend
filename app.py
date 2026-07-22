import os
import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

def buscar_na_web(termo):
    """ Busca no DuckDuckGo via HTML e extrai o resumo do primeiro resultado """
    try:
        url = "https://html.duckduckgo.com/html/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        data = {"q": termo}

        # Faz a requisição direta de busca
        response = requests.post(url, data=data, headers=headers, timeout=6)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            # Extrai os resumos dos resultados da pesquisa
            resultados = soup.find_all("a", class_="result__snippet")
            
            snippets = []
            for res in resultados[:2]: # Pega os 2 primeiros resultados
                texto = res.get_text().strip()
                if texto:
                    snippets.append(texto)
            
            if snippets:
                return " ".join(snippets)
                
        return None
    except Exception as e:
        print(f"Erro no scraper: {e}")
        return None

@app.route('/', methods=['GET'])
@app.route('/get_status', methods=['GET', 'OPTIONS'])
def home():
    if request.method == 'OPTIONS':
        return '', 200
    return jsonify({
        "status": "online",
        "service": "JARVIS Live Web Search",
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

        msg_clean = user_message.lower().strip("? .!")
        palavras_msg = msg_clean.split()

        # 1. Trata apenas saudações simples para ser educado
        saudacoes = ["ola", "olá", "oi", "jarvis"]
        if any(p == msg_clean for p in saudacoes) or (len(palavras_msg) <= 2 and any(p in saudacoes for p in palavras_msg)):
            resposta_texto = "Olá, Mestre Murilo! Como posso ajudar você hoje?"

        # 2. Pesquisa livre na Internet para QUALQUER outra pergunta
        else:
            resultado_web = buscar_na_web(user_message)
            
            if resultado_web:
                resposta_texto = f"Mestre Murilo, encontrei o seguinte na web: {resultado_web}"
            else:
                resposta_texto = f"Mestre Murilo, pesquisei na web sobre '{user_message}', mas não encontrei um resumo claro."

        return jsonify({
            "response": resposta_texto,
            "resposta": resposta_texto
        })

    except Exception as e:
        print(f"Erro no servidor: {e}")
        erro_msg = f"Desculpe, Mestre Murilo. Falha ao acessar a internet: {str(e)}"
        return jsonify({"response": erro_msg, "resposta": erro_msg}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
