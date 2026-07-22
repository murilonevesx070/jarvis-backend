import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

historico_memoria = []
ultimo_comando_pc = None

@app.route('/', methods=['GET'])
@app.route('/get_status', methods=['GET', 'OPTIONS'])
def home():
    if request.method == 'OPTIONS':
        return '', 200
    return jsonify({
        "status": "online",
        "system": "J.A.R.V.I.S. Prism OS - Full Automation Core",
        "uptime": "24/7 Cloud Operational"
    })

@app.route('/comando_pendente', methods=['GET'])
def comando_pendente():
    global ultimo_comando_pc
    cmd = ultimo_comando_pc
    ultimo_comando_pc = None  # Limpa após enviar
    return jsonify({"acao": cmd})

@app.route('/chat', methods=['POST', 'OPTIONS'])
@app.route('/pergunta', methods=['POST', 'OPTIONS'])
def chat():
    global historico_memoria, ultimo_comando_pc
    if request.method == 'OPTIONS':
        return '', 200

    try:
        data = request.get_json(silent=True) or {}
        user_message = (data.get("message") or data.get("pergunta") or data.get("comando") or "").strip()

        if not user_message:
            return jsonify({"response": "À sua inteira disposição, Mestre Murilo.", "resposta": "À sua inteira disposição, Mestre Murilo."}), 400

        msg_lower = user_message.lower()

        # Detecção de Comandos Automáticos do PC
        if "fazer um vídeo" in msg_lower or "fazer um video" in msg_lower or "criar vídeo" in msg_lower:
            ultimo_comando_pc = {"tipo": "abrir_site", "url": "https://runwayml.com"} # Exemplo de IA de vídeo
        elif "tocar musica" in msg_lower or "coloca uma musica" in msg_lower or "tocar música" in msg_lower:
            # Extrai o termo de busca se houver
            termo = msg_lower.replace("tocar musica", "").replace("coloca uma musica", "").strip()
            if not termo:
                termo = "musicas variadas"
            ultimo_comando_pc = {"tipo": "youtube_musica", "busca": termo}
        elif "abra a calculadora" in msg_lower or "abrir calculadora" in msg_lower:
            ultimo_comando_pc = {"tipo": "exec", "cmd": "calc"}
        elif "abra o bloco de notas" in msg_lower:
            ultimo_comando_pc = {"tipo": "exec", "cmd": "notepad"}
        elif "abra o vscode" in msg_lower:
            ultimo_comando_pc = {"tipo": "exec", "cmd": "code"}

        api_key = os.environ.get("GROQ_API_KEY")
        client = Groq(api_key=api_key)

        system_prompt = (
            "Você é o J.A.R.V.I.S., assistente autônomo do Mestre Murilo. "
            "Se o Murilo pedir para executar uma tarefa no computador (criar vídeos, tocar músicas, abrir programas), "
            "confirme de forma elegante, respeitosa e eficiente que a automação foi iniciada no sistema dele."
        )

        messages = [{"role": "system", "content": system_prompt}]
        for msg in historico_memoria[-8:]:
            messages.append(msg)
        messages.append({"role": "user", "content": user_message})

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.8,
            max_tokens=512
        )

        resposta_texto = completion.choices[0].message.content
        historico_memoria.append({"role": "user", "content": user_message})
        historico_memoria.append({"role": "assistant", "content": resposta_texto})

        return jsonify({"response": resposta_texto, "resposta": resposta_texto})

    except Exception as e:
        return jsonify({"response": f"Mestre Murilo, erro na execução: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
