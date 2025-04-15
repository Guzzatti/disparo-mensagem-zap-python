import pandas as pd
import urllib.parse
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# === CONFIGURAÇÕES ===
excel_path = 'data/ClientesTestes.xlsx'
log_path = 'envio_log.txt'
tempo_entre_envios = 150  # 2 minutos e 30 segundos

# Mensagem base com personalização
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

# === CONFIGURA O CHROME COM SEU PERFIL ===
chrome_options = Options()
chrome_options.add_argument(r"--user-data-dir=C:/Users/Usuario/AppData/Local/Google/Chrome/User Data")
chrome_options.add_argument(r"--profile-directory=Profile 10")
chrome_options.add_experimental_option("detach", True)


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Abre o WhatsApp Web com a sessão do seu usuário
driver.get("https://web.whatsapp.com")
input("✅ Pressione Enter após verificar que o WhatsApp Web carregou e está logado...")

# Carrega os dados da planilha
df = pd.read_excel(excel_path)

# Loop de envio
for index, row in df.iterrows():
    nome = row['Client Name']
    numero = str(int(row['Phone']))
    hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    mensagem = mensagem_base.format(nome=nome)
    mensagem_encoded = urllib.parse.quote(mensagem)

    try:
        # Abre o link direto do WhatsApp Web com mensagem
        driver.get(f"https://web.whatsapp.com/send?phone={numero}&text={mensagem_encoded}")

        # Espera até o campo de mensagem aparecer
        campo_msg = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//div[@role="textbox"]'))
        )

        # Pressiona Enter para enviar a mensagem
        campo_msg.send_keys("\n")

        log_msg = f"✅ [{hora}] Mensagem enviada para {nome} ({numero})"
        print(log_msg)

    except Exception as e:
        log_msg = f"❌ [{hora}] Erro ao enviar para {nome} ({numero}): {e}"
        print(log_msg)

    # Salva o log
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(log_msg + '\n')

    # Espera antes do próximo envio
    time.sleep(tempo_entre_envios)
