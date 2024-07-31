import os
import shutil
import pandas as pd

from modules.load_config import config_read


def find_column_name(df, possible_names):
    for col_ in df.columns:
        if col_.lower().strip() in possible_names:
            return col_
    return None


def row_comp(row_c):
    if isinstance(row_c, float):
        row_c = str(int(row_c))

    if len(str(row_c)) == 5:
        date_format = f'01/0{str(row_c)[0]}/{str(row_c)[-4:]}'
        date_comp = pd.to_datetime(date_format, format='%d/%m/%Y')
    elif len(str(row_c)) == 6:
        date_format = f'01/{str(row_c)[:2]}/{str(row_c)[-4:]}'
        date_comp = pd.to_datetime(date_format, format='%d/%m/%Y')
    else:
        date_comp = row_c
    return date_comp


def para_cada_doc(file_path_):
    paths = file_path_.split('\n')
    return paths


# Lendo a planilha
async def abrir_pastas(plan_path):
    config = config_read()

    planilha = pd.read_excel(plan_path)
    tipo_atend = find_column_name(planilha, config['tipo_atend'])
    comp = find_column_name(planilha, config['comp'])
    num_atend = find_column_name(planilha, config['num_atend'])
    tipo_contrat = find_column_name(planilha, config['tipo_contrat'])

    status = find_column_name(planilha, config['status'])
    ilegalidades = find_column_name(planilha, config['ilegalidades'])

    doc_proposta = find_column_name(planilha, ['doc_proposta'])
    doc_contrato = find_column_name(planilha, ['doc_contrato'])
    doc_aditivo = find_column_name(planilha, ['doc_aditivo'])
    doc_comprovante_vinculo = find_column_name(planilha, ['doc_comprovante_vinculo'])
    doc_laudo = find_column_name(planilha, ['doc_laudo'])
    doc_declaracao_saude = find_column_name(planilha, ['doc_declaracao_saude'])
    doc_diverso = find_column_name(planilha, ['doc_diverso'])
    doc_outros = find_column_name(planilha, ['doc_outros'])

    confere_atendimento = []

    # Iterando pelas linhas da planilha
    for _ , row in planilha.iterrows():
        if 'ABRIR PASTAS' in str(row[status]).upper():
            tipo_atendimento = row[tipo_atend]
            numero_atendimento = row[num_atend]
            competencia = row_comp(row[comp])
            tipo_contrato = row[tipo_contrat]
            ilegalidade = row[ilegalidades]
            
            if "/" in ilegalidade:
                nova_ilegalidade = ilegalidade.replace("/", "-")
                ilegalidade = nova_ilegalidade

            nome_pasta = ''
            pasta_path = ''

            if isinstance(numero_atendimento, float):
                numero_atendimento = int(numero_atendimento)
            # Criando o nome da pasta
            if tipo_atendimento.lower() == 'aih':
                if numero_atendimento in confere_atendimento:
                    nome_pasta = f"{tipo_atendimento} {numero_atendimento} C{competencia.month}"
                else:
                    nome_pasta = f"{tipo_atendimento} {numero_atendimento}"
                    confere_atendimento.append(numero_atendimento)
            elif tipo_atendimento.lower() == 'apac':
                nome_pasta = f"{tipo_atendimento} {numero_atendimento} C{competencia.month}"

            # Verificando se a pasta já existe, se não, cria a pasta
            dir_plan_path = os.path.dirname(plan_path)
            if any(word in tipo_contrato.lower() for word in config['tipo_contratos']['colem/colad']):
                pasta_path = os.path.join(dir_plan_path,
                                          f"ABERTURA DE PASTAS\\{ilegalidade}\\COLEM - COLAD\\{nome_pasta}")
            elif any(word in tipo_contrato.lower() for word in config['tipo_contratos']['indiv']):
                pasta_path = os.path.join(dir_plan_path, f"ABERTURA DE PASTAS\\{ilegalidade}\\INDIVIDUAL\\{nome_pasta}")

            # if not os.path.exists(pasta_path):
            os.makedirs(pasta_path, exist_ok=True)

            # Copiando os arquivos PDF para a pasta criada
            for i, col in enumerate([doc_proposta, doc_contrato, doc_aditivo, doc_comprovante_vinculo, doc_laudo,
                                     doc_outros, doc_declaracao_saude, doc_diverso], start=1):
                file_path = row[col]
                if pd.notnull(file_path):
                    if col == doc_diverso:
                        paths_list = para_cada_doc(file_path)
                        for each_path in paths_list:
                            file_name = os.path.basename(each_path.strip())  # f"{each_path.strip()}"
                            dest_path = os.path.join(pasta_path, file_name)
                            shutil.copy(each_path, dest_path)
                    elif col == doc_outros:
                        paths_list = para_cada_doc(file_path)
                        for each_path in paths_list:
                            if "memória de cálculo" in each_path.lower():
                                ec_path = "MEMÓRIA DE CÁLCULO.pdf"
                            else:
                                ec_path = os.path.basename(each_path.strip())

                            file_name = f"{numero_atendimento}.{i + 4} {ec_path}"
                            # file_ext = os.path.splitext(each_path.strip())[1]
                            dest_path = os.path.join(pasta_path, file_name)
                            shutil.copy(each_path, dest_path)
                    else:
                        file_name = f"{numero_atendimento}.{i}"
                        file_ext = os.path.splitext(file_path)[1]
                        dest_path = os.path.join(pasta_path, file_name + file_ext)
                        shutil.copy(file_path, dest_path)

    return "Concluído"
