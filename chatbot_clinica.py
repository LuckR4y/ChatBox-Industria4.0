import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Configuração para conectar ao Google Sheets via API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json", scope)
client = gspread.authorize(creds)

# Abrir a planilha (já criada previamente no Google Drive)
sheet = client.open("Agendamentos_Clinica").sheet1  # Nome exato da planilha

# Função para registrar agendamento
def registrar_agendamento(nome, data, hora):
    agora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sheet.append_row([agora, nome, data, hora, "Agendamento"])
    print(f"✅ Agendamento confirmado para {data} às {hora}.")

# Loop de interação simples simulando chatbot
print("Bot: Olá, bem-vindo à Clínica Odonto. Como posso ajudar? (Digite 'sair' para encerrar)")
while True:
    pergunta = input("Você: ").lower()
    if "marcar" in pergunta:
        nome = input("Bot: Informe seu nome completo: ")
        data = input("Bot: Informe a data desejada (dd/mm): ")
        hora = input("Bot: Informe o horário desejado (hh:mm): ")
        registrar_agendamento(nome, data, hora)
    elif "sair" in pergunta:
        print("Bot: Obrigado, até a próxima!")
        break
    else:
        print("Bot: Desculpe, não entendi. Você deseja 'marcar' uma consulta ou 'sair'?")
