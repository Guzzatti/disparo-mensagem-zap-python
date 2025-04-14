import pandas as pd
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# Lê a planilha
df = pd.read_excel("data/ClientesTestes.xlsx")
log_path = "envio_log.txt"

# Mensagem base
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

# Configurações do Chrome com perfil salvo
chrome_options = Options()
chrome_options.add_argument("user-data-dir=whatsapp_session")  # salva sessão
chrome_options.add_argument("--start-maximized")

# Inicializa o driver automaticamente com a versão certa
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get("https://web.whatsapp.com")

# Espera login manual se for a primeira vez
input("📲 Escaneie o QR code no WhatsApp Web e pressione ENTER aqui quando estiver logado...")

for index, row in df.iterrows():
    nome = row["Client Name"]
    numero = str(row["Phone"])
    mensagem = mensagem_base.format(nome=nome)
    hora = datetime.now().strftime("%H:%M:%S")

    try:
        driver.get(f"https://wa.me/{numero}")
        time.sleep(8)

        try:
            start_chat = driver.find_element(By.XPATH, '//a[contains(@href, "web.whatsapp.com/send")]')
            start_chat.click()
            time.sleep(8)
        except:
            pass

        campo_msg = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
        campo_msg.send_keys(mensagem)
        campo_msg.send_keys(Keys.ENTER)

        log_msg = f"✅ Mensagem enviada para {nome} ({numero}) às {hora}"
        print(log_msg)

    except Exception as e:
        log_msg = f"❌ Erro ao enviar para {nome} ({numero}): {e}"
        print(log_msg)

    with open(log_path, "a", encoding="utf-8") as log_file:
        log_file.write(log_msg + "\n")

    time.sleep(150)  # espera 2min30s
