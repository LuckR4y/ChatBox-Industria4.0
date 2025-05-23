from flask import Flask, request, jsonify
from flask_cors import CORS
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

app = Flask(__name__)
CORS(app)

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Agendamentos_Clinica").sheet1

def limpar_chave(chave):
    return chave.strip().replace('\t', '').lower()

def encontrar_linha_ativa(nome):
    dados = sheet.get_all_records()
    nome_lower = nome.strip().lower()
    if not dados:
        print("[DEBUG encontrar_linha_ativa] Nenhum dado na planilha")
        return None

    print(f"[DEBUG encontrar_linha_ativa] Cabeçalhos: {list(dados[0].keys())}")

    for i, registro in enumerate(dados, start=2):
        # Corrige chaves removendo tabs e espaços
        registro_corrigido = {limpar_chave(k): (v.strip() if isinstance(v, str) else v) for k,v in registro.items()}

        nome_registro = registro_corrigido.get('nome do cliente', '').lower()
        status_registro = registro_corrigido.get('tipo de interação', '')

        print(f"[DEBUG encontrar_linha_ativa] Linha {i}: nome='{nome_registro}', status='{status_registro}'")

        if nome_registro == nome_lower and status_registro == "Agendamento":
            print(f"[DEBUG encontrar_linha_ativa] Encontrado na linha {i}")
            return i

    print("[DEBUG encontrar_linha_ativa] Nenhum agendamento ativo encontrado")
    return None

def registrar_acao(nome, data_consulta, horario, status):
    agora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[DEBUG registrar_acao] Salvando linha: {agora}, {nome}, {data_consulta}, {horario}, {status}")
    sheet.append_row([agora, nome, data_consulta, horario, status])

@app.route('/salvar-agendamento', methods=['POST'])
def salvar_agendamento():
    data = request.json
    print("[DEBUG salvar_agendamento] dados recebidos:", data)
    nome = data.get('nome')
    data_consulta = data.get('data_consulta')
    horario = data.get('horario')

    if not nome or not data_consulta or not horario:
        return jsonify({"status": "erro", "mensagem": "Dados incompletos"}), 400

    linha = encontrar_linha_ativa(nome)
    if linha:
        return jsonify({"status": "erro", "mensagem": "Já existe um agendamento ativo para esse nome. Use a opção de remarcar."}), 400

    try:
        registrar_acao(nome, data_consulta, horario, "Agendamento")
        return jsonify({"status": "sucesso", "mensagem": "Agendamento salvo"})
    except Exception as e:
        print("[ERROR salvar_agendamento] Erro ao salvar agendamento:", e)
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

@app.route('/cancelar-agendamento', methods=['POST'])
def cancelar_agendamento():
    data = request.json
    print("[DEBUG cancelar_agendamento] dados recebidos:", data)
    nome = data.get('nome')

    if not nome:
        return jsonify({"status": "erro", "mensagem": "Nome é obrigatório"}), 400

    linha = encontrar_linha_ativa(nome)
    if linha:
        try:
            sheet.update_cell(linha, 5, "Cancelado")
            return jsonify({"status": "sucesso", "mensagem": f"Agendamento de {nome} cancelado."})
        except Exception as e:
            print("[ERROR cancelar_agendamento] Erro ao cancelar:", e)
            return jsonify({"status": "erro", "mensagem": str(e)}), 500
    else:
        return jsonify({"status": "erro", "mensagem": "Nenhum agendamento ativo encontrado para esse nome."}), 404

@app.route('/remarcar-agendamento', methods=['POST'])
def remarcar_agendamento():
    data = request.json
    print("[DEBUG remarcar_agendamento] dados recebidos:", data)
    nome = data.get('nome')
    nova_data = data.get('nova_data')
    novo_horario = data.get('novo_horario')

    if not nome or not nova_data or not novo_horario:
        return jsonify({"status": "erro", "mensagem": "Dados incompletos"}), 400

    linha = encontrar_linha_ativa(nome)
    if linha:
        try:
            sheet.update_cell(linha, 3, nova_data)
            sheet.update_cell(linha, 4, novo_horario)
            sheet.update_cell(linha, 5, "Remarcado")
            return jsonify({"status": "sucesso", "mensagem": f"Agendamento de {nome} remarcado para {nova_data} às {novo_horario}."})
        except Exception as e:
            print("[ERROR remarcar_agendamento] Erro ao remarcar:", e)
            return jsonify({"status": "erro", "mensagem": str(e)}), 500
    else:
        return jsonify({"status": "erro", "mensagem": "Nenhum agendamento ativo encontrado para esse nome."}), 404

@app.route('/listar-agendamentos', methods=['GET'])
def listar_agendamentos():
    dados = sheet.get_all_records()
    dados_normalizados = []
    for reg in dados:
        nova_entrada = {}
        for k, v in reg.items():
            chave_limpa = k.strip().replace('\t', '')
            valor_limpo = v.strip() if isinstance(v, str) else v
            nova_entrada[chave_limpa] = valor_limpo
        dados_normalizados.append({
            "data_interacao": nova_entrada.get("Data da interação", ""),
            "nome_cliente": nova_entrada.get("Nome do Cliente", ""),
            "data_consulta": nova_entrada.get("Data da consulta", ""),
            "horario": nova_entrada.get("Horário", ""),
            "status": nova_entrada.get("Tipo de interação", ""),
        })
    print(f"[DEBUG listar_agendamentos] Retornando {len(dados_normalizados)} registros")
    return jsonify(dados_normalizados)

if __name__ == '__main__':
    app.run(debug=True)
