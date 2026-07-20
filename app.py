from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime

app = Flask(__name__)
# O CORS(app) libera o acesso para que o site do Lovable consiga conversar com seu PC
CORS(app)

@app.route('/get_status', methods=['GET'])
def get_status():
    """Rota para o Lovable verificar se o Jarvis está online"""
    return jsonify({
        "status": "online",
        "sistema": "Prism OS",
        "mensagem": "Sistema Prism OS online, Mestre Murilo. Aguardando comandos."
    }), 200

@app.route('/pergunta', methods=['POST'])
def pergunta():
    """Rota principal onde o Jarvis recebe e processa seus comandos"""
    try:
        data = request.get_json()
        if not data or 'comando' not in data:
            # Caso o Lovable envie o texto em outro campo (ex: 'texto' ou 'pergunta')
            user_message = data.get('texto', data.get('pergunta', ''))
        else:
            user_message = data['comando']
            
        print(f"[MURILO]: {user_message}") # Mostra no seu terminal o que você digitou
        
        user_message_lower = user_message.lower()
        resposta_texto = ""

        # --- LÓGICA DE COMANDOS DO JARVIS ---
        if "ola jarvis" in user_message_lower or "olá jarvis" in user_message_lower:
            resposta_texto = "Olá, Mestre Murilo. Sistema totalmente operacional. Como posso ajudar hoje?"
            
        elif "que horas" in user_message_lower or "hora" in user_message_lower:
            hora_atual = datetime.datetime.now().strftime("%H:%M")
            resposta_texto = f"Agora são exatamente {hora_atual}, Mestre."
            
        elif "quem é você" in user_message_lower or "quem e voce" in user_message_lower:
            resposta_texto = "Eu sou o JARVIS, sua inteligência artificial baseada no Prism OS."
            
        else:
            resposta_texto = "Comando recebido, Mestre Murilo. Processando informações."

        print(f"[JARVIS]: {resposta_texto}") # Mostra no seu terminal a resposta dele
        
        return jsonify({
            "resposta": resposta_texto,
            "status": "sucesso"
        }), 200

    except Exception as e:
        print(f"Erro ao processar: {e}")
        return jsonify({"resposta": "Desculpe Mestre, ocorreu um erro interno no meu sistema.", "status": "erro"}), 500

if __name__ == '__main__':
    # host='0.0.0.0' é fundamental para o ngrok conseguir repassar as requisições
    app.run(host='0.0.0.0', port=5000, debug=False)
