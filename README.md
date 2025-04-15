# 📲 Guzzatti - Automação de Mensagens no WhatsApp

Este projeto automatiza o envio de mensagens personalizadas via WhatsApp Web para clientes que não compram há 6 meses, utilizando o navegador Chrome com uma sessão já logada.

---

## 🚀 Funcionalidades

- Lê a planilha `ClientesTestes.xlsx` na pasta `data/`
- Usa seu perfil do Chrome logado no WhatsApp Web (sem QR Code)
- Envia mensagens com o nome do cliente personalizado
- Espera 2 minutos e 30 segundos entre os envios
- Salva um log com o status de cada envio em `envio_log.txt`

---

## 🧾 Estrutura da Planilha

A planilha precisa estar salva como:

data/ClientesTestes.xlsx

E deve conter as colunas:

- `Client Name` — primeiro nome do cliente
- `Phone` — número do WhatsApp no formato internacional (ex: 55999999999)

---

## 🖥️ Configuração do Perfil do Chrome

No script, você deve indicar o caminho do perfil do Chrome. Exemplo:

```python
chrome_options.add_argument(r"--user-data-dir=C:/Users/Usuario/AppData/Local/Google/Chrome/User Data")
chrome_options.add_argument(r"--profile-directory=Profile 10")

Você pode descobrir o seu caminho acessando chrome://version no navegador.

▶️ Rodando o projeto

Instale as dependências:

pip install selenium webdriver-manager pandas openpyxl


Execute com:

python main.py


📄 Observações
Deixe o Chrome aberto e não o use durante o envio.

Certifique-se de que o WhatsApp Web está carregado corretamente com sua conta.