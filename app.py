from flask import Flask, request, jsonify
from flask_cors import CORS
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Permite requisições do frontend

# Configuração da API Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Agendamentos_Clinica").sheet1  # nome da planilha e aba

def registrar_acao(nome, data_consulta, horario, status):
    agora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sheet.append_row([agora, nome, data_consulta, horario, status])

@app.route('/salvar-agendamento', methods=['POST'])
def salvar_agendamento():
    data = request.json
    nome = data.get('nome')
    data_consulta = data.get('data_consulta')
    horario = data.get('horario')

    if not nome or not data_consulta or not horario:
        return jsonify({"status": "erro", "mensagem": "Dados incompletos"}), 400

    try:
        registrar_acao(nome, data_consulta, horario, "Agendamento")
        return jsonify({"status": "sucesso", "mensagem": "Agendamento salvo"})
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
