import pandas as pd
import pywhatkit
import time
from datetime import datetime

# Configurações
excel_path = 'ClientesTeste.xlsx'
log_path = 'envio_log.txt'
tempo_entre_envios = 150  # 2 minutos e 30 segundos

# Mensagem personalizada
mensagem_base = (
    "💖 Oi, {nome}! Tudo bem?\n\n"
    "A gente está com saudades de ver você por aqui! 🥹\n"
    "O Dia das Mães está chegando, e essa é a hora perfeita pra encontrar um presente marcante – "
    "com aquele brilho especial que só a Guzzatti tem! ✨\n\n"
    "Corre lá no nosso site e aproveita as novidades (tem coisa linda e com condições especiais 😍)\n\n"
    "🛍️ www.guzzatti.com.br\n"
    "🎁 Não deixa pra última hora!\n\n"
    "Com carinho,\n"
    "Equipe Guzzatti 🤍"
)

# Carregar a planilha
df = pd.read_excel(excel_path)

# Loop de envio
for index, row in df.iterrows():
    nome = row['Client Name']
    numero = row['Phone']
    
    if pd.isna(numero):
        print(f"❌ Número ausente para {nome}, pulando...")
        continue

    mensagem = mensagem_base.format(nome=nome)
    numero_formatado = f"+{int(numero)}"
    hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        pywhatkit.sendwhatmsg_instantly(
            phone_no=numero_formatado,
            message=mensagem,
            wait_time=30,
            tab_close=True
        )
        log_msg = f"✅ [{hora}] Mensagem enviada para {nome} ({numero_formatado})"
        print(log_msg)
    except Exception as e:
        log_msg = f"❌ [{hora}] Erro ao enviar para {nome} ({numero_formatado}): {e}"
        print(log_msg)

    # Registrar no log
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(log_msg + '\n')

    time.sleep(tempo_entre_envios)
