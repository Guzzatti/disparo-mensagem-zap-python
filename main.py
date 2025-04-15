import pandas as pd
from neonize.client import NewClient
from neonize.events import ConnectedEv
import asyncio
import os
import random
from datetime import datetime
# import qrcode  ← Comentado pois o QR ainda não pode ser interceptado

# [Opcional futuramente] Função para exibir o QR Code como imagem
# def mostrar_qr_como_imagem(qr_string: str):
#     img = qrcode.make(qr_string)
#     img.show()

# Carrega os clientes da planilha
df = pd.read_excel("data/ClientesTestes.xlsx")

# Garante que a pasta de logs existe
os.makedirs("logs", exist_ok=True)

# Função para salvar logs de envio
def log_envio(nome, telefone, status):
    with open("logs/log_envio.txt", "a", encoding="utf-8") as f:
        now = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        f.write(f"{now} | {telefone} | {nome} | {status}\n")

# Gera a mensagem personalizada
def gerar_mensagem(nome):
    return f"""💖 Oi, {nome}! Tudo bem?

A gente está com saudades de ver você por aqui! 🥹
O Dia das Mães está chegando, e essa é a hora perfeita pra encontrar um presente marcante – com aquele brilho especial que só a Guzzatti tem! ✨

Corre lá no nosso site e aproveita as novidades (tem coisa linda e com condições especiais 😍)

🛍️ www.guzzatti.com.br
🎁 Não deixa pra última hora!

Com carinho,
Equipe Guzzatti 🤍"""

# Cria o cliente WhatsApp
client = NewClient("session_guzzatti.sqlite3")

@client.event(ConnectedEv)
async def ao_conectar(client: NewClient, _: ConnectedEv):
    print("✅ Conectado ao WhatsApp. Iniciando envios...\n")

    for _, row in df.iterrows():
        nome = row["Client Name"]
        telefone = str(row["Phone"])
        mensagem = gerar_mensagem(nome)

        try:
            await client.send_message(telefone, mensagem)
            log_envio(nome, telefone, "ENVIADO")
            print(f"✅ Mensagem enviada para {nome} ({telefone})")
        except Exception as e:
            log_envio(nome, telefone, f"ERRO: {e}")
            print(f"❌ Erro ao enviar para {nome} ({telefone}): {e}")

        delay = random.randint(90, 150)
        print(f"⏳ Aguardando {delay} segundos antes do próximo envio...\n")
        await asyncio.sleep(delay)

# Conecta usando QR no terminal (padrão)
client.connect()
