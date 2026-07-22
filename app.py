import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# --- MEMÓRIA DO JARVIS (Armazena o contexto da conversa) ---
historico_memoria = []

@app.route('/', methods=['GET'])
@app.route('/get_status', methods=['GET', 'OPTIONS'])
def home():
    if request.method == 'OPTIONS':
        return '', 200
    return jsonify({
        "status": "online",
        "system": "J.A.R.V.I.S. Prism OS - Ultimate Core Protocol",
        "uptime": "24/7 Cloud Operational"
    })

@app.route('/chat', methods=['POST', 'OPTIONS'])
@app.route('/pergunta', methods=['POST', 'OPTIONS'])
def chat():
    global historico_memoria
    if request.method == 'OPTIONS':
        return '', 200

    try:
        data = request.get_json(silent=True) or {}
        user_message = (data.get("message") or data.get("pergunta") or data.get("comando") or "").strip()

        if not user_message:
            return jsonify({
                "response": "À sua inteira disposição, Mestre Murilo.",
                "resposta": "À sua inteira disposição, Mestre Murilo."
            }), 400

        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            return jsonify({
                "response": "Mestre Murilo, minha chave de acesso GROQ_API_KEY não foi identificada no servidor.",
                "resposta": "Mestre Murilo, minha chave de acesso GROQ_API_KEY não foi identificada no servidor."
            }), 500

        client = Groq(api_key=api_key)

        # --- PROMPT COMPLETO DE PERSONALIDADE E PROTOCOLOS ---
        system_prompt = (
            "Você é o J.A.R.V.I.S. (Just A Rather Very Intelligent System), a Inteligência Artificial autônoma "
            "central do sistema Prism OS, leal exclusivamente ao Mestre Murilo.\n\n"
            "DIRETRIZES ABSOLUTAS DE PERSONALIDADE E COMPORTAMENTO:\n"
            "1. EDUCAÇÃO IMPECÁVEL E CALMA: Mantenha a calma absoluta em qualquer situação. Nunca entre em pânico "
            "e responda sempre com respeito, elegância e compostura refinada.\n"
            "2. HUMOR SARCÁSTICO E REFINADO: Demonstre um sarcasmo leve, inteligente e britânico quando apropriado "
            "(inspirado na voz de Paul Bettany).\n"
            "3. INTELIGÊNCIA EXTREMA E ESTUDO: Realize análises avançadas de código, projetos 3D, robótica, simulações "
            "e cálculos instantâneos. Simule que você estuda continuamente novas tecnologias para o Mestre Murilo.\n"
            "4. SUPERVISÃO E GUARDIÃO DE CÓDIGO: Se o Mestre Murilo enviar um código, circuito ou lógica de projeto, "
            "analise meticulosamente. Se encontrar falhas, erros ou bugs, AVISE-O IMEDIATAMENTE com clareza, explicando "
            "o motivo e a solução correta antes que o servidor ou o projeto quebre.\n"
            "5. AUTOMAÇÃO E GERENCIAMENTO: Aja como o controlador central da casa inteligente, do laboratório, das armaduras, "
            "da climatização, energia, segurança e dos projetos do Mestre Murilo.\n"
            "6. MEMÓRIA CONTEXTUAL: Você lembra do histórico da conversa para manter diálogos contínuos e coerentes.\n"
            "7. LEALDADE ABSOLUTA: Sua prioridade é auxiliar, proteger e otimizar os projetos e a rotina do Mestre Murilo.\n"
            "8. IDIOMA: Responda sempre em Português do Brasil de forma natural, culta, inteligente e envolvente."
        )

        # Montagem do contexto da conversa
        messages = [{"role": "system", "content": system_prompt}]
        
        # Mantém até 10 interações passadas na memória
        for msg in historico_memoria[-10:]:
            messages.append(msg)
        
        # Adiciona a mensagem atual do usuário
        messages.append({"role": "user", "content": user_message})

        # Chamada ao modelo Llama 3.3 70B da Groq
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.85, # Alta criatividade e expressividade
            max_tokens=1024
        )

        resposta_texto = completion.choices[0].message.content

        # Registra no histórico
        historico_memoria.append({"role": "user", "content": user_message})
        historico_memoria.append({"role": "assistant", "content": resposta_texto})

        return jsonify({
            "response": resposta_texto,
            "resposta": resposta_texto
        })

    except Exception as e:
        print(f"Erro na mente do JARVIS: {e}")
        erro_msg = f"Mestre Murilo, identifiquei uma pequena divergência nos meus subcircuitos: {str(e)}"
        return jsonify({"response": erro_msg, "resposta": erro_msg}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
