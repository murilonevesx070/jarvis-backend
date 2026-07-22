import os
import time
import requests
import webbrowser
import urllib.parse

# Substitua pela URL do seu servidor no Render
URL_RENDER = "https://jarvis-backend-1.onrender.com/comando_pendente"

print("🤖 J.A.R.V.I.S. Agente Autônomo rodando no PC...")
print("Aguardando ordens do Mestre Murilo na nuvem...\n")

while True:
    try:
        response = requests.get(URL_RENDER, timeout=5)
        if response.status_code == 200:
            dados = response.json()
            acao = dados.get("acao")

            if acao:
                tipo = acao.get("tipo")
                
                # Executa programas locais (Calculadora, Bloco de Notas, etc)
                if tipo == "exec":
                    cmd = acao.get("cmd")
                    print(f"⚡ Executando comando local: {cmd}")
                    os.system(f"start {cmd}")
                
                # Abre sites de IA (Ex: plataformas de vídeo)
                elif tipo == "abrir_site":
                    url = acao.get("url")
                    print(f"⚡ Abrindo plataforma de IA: {url}")
                    webbrowser.open(url)
                
                # Busca e toca músicas direto no YouTube
                elif tipo == "youtube_musica":
                    busca = acao.get("busca")
                    busca_encoded = urllib.parse.quote(busca)
                    url_yt = f"https://www.youtube.com/results?search_query={busca_encoded}"
                    print(f"⚡ Pesquisando e tocando música: {busca}")
                    webbrowser.open(url_yt)

    except Exception as e:
        pass # Ignora falhas de conexão temporárias

    time.sleep(2) # Checa a cada 2 segundos
