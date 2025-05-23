import requests

API_BASE_URL = 'http://localhost:5000'

def salvar_agendamento_api(nome, data_consulta, horario):
    url = f"{API_BASE_URL}/salvar-agendamento"
    resp = requests.post(url, json={'nome': nome, 'data_consulta': data_consulta, 'horario': horario})
    if resp.status_code == 200:
        print(f"Bot: {resp.json().get('mensagem')}")
    else:
        print(f"Bot: Erro ao salvar agendamento: {resp.json().get('mensagem')}")

def cancelar_agendamento_api(nome):
    url = f"{API_BASE_URL}/cancelar-agendamento"
    resp = requests.post(url, json={'nome': nome})
    if resp.status_code == 200:
        print(f"Bot: {resp.json().get('mensagem')}")
    else:
        print(f"Bot: Erro ao cancelar: {resp.json().get('mensagem')}")

def remarcar_agendamento_api(nome, nova_data, novo_horario):
    url = f"{API_BASE_URL}/remarcar-agendamento"
    resp = requests.post(url, json={'nome': nome, 'nova_data': nova_data, 'novo_horario': novo_horario})
    if resp.status_code == 200:
        print(f"Bot: {resp.json().get('mensagem')}")
    else:
        print(f"Bot: Erro ao remarcar: {resp.json().get('mensagem')}")

def avisar_atraso_api(nome):
    url = f"{API_BASE_URL}/avisar-atraso"
    resp = requests.post(url, json={'nome': nome})
    if resp.status_code == 200:
        print(f"Bot: {resp.json().get('mensagem')}")
    else:
        print(f"Bot: Erro ao enviar aviso de atraso: {resp.json().get('mensagem')}")

def main():
    print("Bot: Olá, bem-vindo à Clínica Odonto.")
    print("Bot: Posso te ajudar com as seguintes opções:")
    print("Bot: 1- Marcar consulta")
    print("Bot: 2- Cancelar consulta")
    print("Bot: 3- Remarcar consulta")
    print("Bot: 4- Vou me atrasar")
    print("Bot: 0- Sair do agendamento")

    while True:
        pergunta = input("Você: ").lower()

        if "1" in pergunta:
            nome = input("Bot: Informe seu nome completo: ")
            data = input("Bot: Informe a data desejada (dd/mm): ")
            hora = input("Bot: Informe o horário desejado (hh:mm): ")
            salvar_agendamento_api(nome, data, hora)

        elif "2" in pergunta:
            nome = input("Bot: Para cancelar, por favor, informe seu nome completo: ")
            cancelar_agendamento_api(nome)

        elif "3" in pergunta:
            nome = input("Bot: Para remarcar, por favor, informe seu nome completo: ")
            nova_data = input("Bot: Informe a nova data desejada (dd/mm): ")
            nova_hora = input("Bot: Informe o novo horário desejado (hh:mm): ")
            remarcar_agendamento_api(nome, nova_data, nova_hora)

        elif "4" in pergunta or "atraso" in pergunta:
            nome_atraso = input("Bot: Por favor, informe seu nome completo para avisar atraso: ")
            avisar_atraso_api(nome_atraso)

        elif "0" in pergunta:
            print("Bot: Obrigado, até a próxima!")
            break

        else:
            print("Bot: Desculpe, não entendi. Você deseja 'marcar', 'cancelar', 'remarcar' uma consulta, avisar que vai 'atrasar' ou 'sair'?")

if __name__ == '__main__':
    main()
