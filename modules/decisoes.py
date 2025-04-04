import pandas as pd
import re
from datetime import datetime

from pdfminer.high_level import extract_text

from modules.load_config import config_read
from modules.extrair_texto_decisao import processa_texto

colunas_decisao = [
    "DECISÃO",
    "ALEGAÇÃO1",
    "ALEGAÇÃO2",
    "ALEGAÇÃO3",
    "MOTIVO1",
    "MOTIVO2",
    "MOTIVO3",
    "VLR DECOTE",
    "VLR REMANESCENTE",
]


# Localiza as colunas necessárias
def procura_col(planilha, colunas):
    for coluna in colunas:
        if coluna in planilha:
            return coluna
    return None


# Formata data para datetime
def formatar_data(competencia):
    if isinstance(competencia, float):
        competencia = str(int(competencia))

    if len(str(competencia)) == 5:
        data_formatada = f"01/0{str(competencia)[0]}/{str(competencia)[-4:]}"
        competencia_formatada = pd.to_datetime(data_formatada, format="%d/%m/%Y")
    elif len(str(competencia)) == 6:
        data_formatada = f"01/{str(competencia)[:2]}/{str(competencia)[-4:]}"
        competencia_formatada = pd.to_datetime(data_formatada, format="%d/%m/%Y")
    else:
        competencia_formatada = competencia
    return competencia_formatada


# Formata string em data_base
def str_to_data_base(data_string):
    formato = "%d/%m/%Y"
    objeto_data = datetime.strptime(data_string, formato)
    return objeto_data


async def mainn(path_plan, path_dados):
    configurar = config_read()
    lista_num_atend = configurar["lista_num_atend"]
    lista_competencia = configurar["lista_competencia"]
    lista_tipo_procedimento = configurar["lista_tipo_procedimento"]

    lista_valor_tipo_procedimento = configurar["lista_valor_tipo_procedimento"]

    try:
        df = pd.read_excel(path_plan)
        dados = extract_text(path_dados)
    except FileNotFoundError:
        return "Error: Arquivo não encontrado."
    except pd.errors.EmptyDataError:
        return "Error: Arquivo excel está vazio."
    except Exception as e:
        return f"Error: {e}. Arquivo excel está vazio."

    modified_text = re.sub(r"Pág\. \d+ de \d+", "", dados)
    modified_text = re.sub(r"\n\n", "\n", modified_text)
    modified_text = re.sub(r"\x0c", "\n", modified_text)

    data_base = processa_texto(modified_text)

    # Cria as colunas da decisão
    for item in colunas_decisao:
        df[item] = None

    atendimento = procura_col(df, lista_num_atend)
    competencia = procura_col(df, lista_competencia)
    tipo_procedimento = procura_col(df, lista_tipo_procedimento)

    # Se não tiver nenhuma dessas colunas acima retorna mensagem de aviso
    is_none = [atendimento, competencia, tipo_procedimento]
    if any([item is None for item in is_none]):
        not_coluna = ("do atendimento" if atendimento is None
                      else "da competência" if competencia is None
                      else "do tipo de procedimento (Principal/Secundário"
                      )
        return f"Coluna {not_coluna} não encontrada!"

    # Formata os valores da coluna do atendimento de número para string de números inteiros
    try:
        df[atendimento] = df[atendimento].apply(lambda x: str(int(x)))  # type: ignore
    except ValueError:
        return "ValueError: não da pra converter espaço vazio em inteiro (coluna do número do atendimento)"

    for key in data_base.keys():
        for index, row in df.iterrows():
            # Verifica se o valor na coluna está presente como uma chave no dicionário data_base
            if (
                str(row[atendimento]) == str(data_base[key]["atendimento"])
                and row[tipo_procedimento] in lista_valor_tipo_procedimento
            ):
                comparar_comp = str_to_data_base(data_base[key]["comp"])
                # Verifica se o valor de 'compet' na coluna B corresponde ao valor de 'compet' no dicionário data_base
                row_competencia = formatar_data(row[competencia])

                if row_competencia == comparar_comp:  # type: ignore
                    # Adiciona os valores correspondentes às novas colunas
                    # type: ignore
                    df.at[index, "DECISÃO"] = data_base[key]["opinion"]
                    df.at[index, "ALEGAÇÃO1"] = data_base[key]["alegation1"]
                    df.at[index, "ALEGAÇÃO2"] = data_base[key]["alegation2"]
                    df.at[index, "ALEGAÇÃO3"] = data_base[key]["alegation3"]
                    df.at[index, "MOTIVO1"] = data_base[key]["texto1"]
                    df.at[index, "MOTIVO2"] = data_base[key]["texto2"]
                    df.at[index, "MOTIVO3"] = data_base[key]["texto3"]
                    # type: ignore
                    df.at[index, "VLR DECOTE"] = data_base[key]["decote"]
                    # type: ignore
                    df.at[index, "VLR REMANESCENTE"] = data_base[key]["resto"]

    # Salva o data_baseFrame atualizado de volta na planilha
    df.to_excel(f"{path_plan[:-5]} - DECISÃO.xlsx", index=False)
    return "Concluído com sucesso!"
