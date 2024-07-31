import re
from modules.load_config import config_read

configurar = config_read()

opinion_list = configurar["lista_opiniao_decisao"]
alegation_list = configurar["lista_alegacao_decisao"]


def identificador_do_atendimento(linha):
    match = re.search(r'\d{13}', linha)
    comp_match = re.search(r'^\d{2}/\d{4}$', linha)
    if match:
        return match.group(0)
    elif comp_match:
        return f'01/{comp_match.group(0)}'
    elif linha.lower().startswith('apac'):
        return 'APAC'
    elif linha.lower().startswith('aih'):
        return 'AIH'


# Extrai valor de copart (decote e remanescente)
def extract_value(*args):
    decote = None
    remanescente = None

    for arg in args:
        # re (regular expressions) para encontrar padrões de textos/dígitos
        percent_match = re.search(r'(\d+(\.\d+)?)%', arg)
        real_matches = re.findall(r'R\$ *(\d+(\.\d{3})*,\d{2})', arg)

        # Procura por valores em porcentagem
        if percent_match:
            decote = percent_match.group(0)
            remanescente = None

        # Procura por valores em real brasileiro
        if len(real_matches) >= 2:
            decote = real_matches[0][0]
            remanescente = real_matches[1][0]
        elif len(real_matches) == 1:
            if percent_match:
                remanescente = real_matches[0][0]
            else:
                decote = real_matches[0][0]
                remanescente = None

        return decote, remanescente


def processa_texto(texto):
    new_atendimento = False
    dicionario = {}
    key_atendimento = ''

    tipo_atendimento = ''
    numero_atendimento = ''
    competencia = ''

    texto_analise = ''
    texto_analise_2 = ''
    texto_analise_3 = ''

    last_line = ''
    for line in texto.split("\n"):
        line = line.strip()
        
        if not line:
            continue

        dados_do_atendimento = identificador_do_atendimento(line)
        if dados_do_atendimento:
            texto_analise = ''
            texto_analise_2 = ''
            texto_analise_3 = ''

            if match:= re.search(r'^\d{13}$', line):
                new_atendimento = True
                numero_atendimento = dados_do_atendimento

                if new_atendimento:
                    new_atendimento = False
            
            if dados_do_atendimento == 'APAC' or dados_do_atendimento == 'AIH':
                tipo_atendimento = dados_do_atendimento
            elif re.search(r'\d{2}/\d{4}', line.strip()): 
                competencia = dados_do_atendimento
        else:
            if not new_atendimento and not re.search(r'\d$', line.strip()) and not line == '' and not 'VL' in line:
                if competencia:
                    key_atendimento = f'{numero_atendimento}{competencia}'
                    if line.isupper():
                        if f"{last_line} {line}" in alegation_list:
                            line = f"{last_line} {line}"
                        else:
                            last_line = line

                
                    if not key_atendimento in dicionario:
                        dicionario[key_atendimento] = {'atendimento': numero_atendimento, 'comp': competencia, 'opinion': '',
                                                    'alegation1': '', 'alegation2': '', 'alegation3': '',
                                                    'texto1': '', 'texto2': '', 'texto3': '', 'decote': '', 'resto': ''}

                    if line in opinion_list:
                        if "ALEGAÇÃO:" in line:
                            line = line[9:].strip()

                        if line not in dicionario[key_atendimento]['opinion']:
                            dicionario[key_atendimento]['opinion'] = line
                            
                    elif line in alegation_list:
                        for i in range(1, 4):
                            if dicionario[key_atendimento][f'alegation{i}'] == '':
                                dicionario[key_atendimento][f'alegation{i}'] = line
                                last_line = ''
                                break
                    elif not line.isupper():
                        emptys = sum(1 if dicionario[key_atendimento][f'alegation{i}'] != '' else 0 for i in range(1, 4))

                        match emptys:
                            case 0:
                                texto_analise = ' '.join([texto_analise, line.strip()])
                                dicionario[key_atendimento]['texto1'] = texto_analise.strip()
                            case 1:
                                texto_analise = ' '.join([texto_analise, line.strip()])
                                dicionario[key_atendimento]['texto1'] = texto_analise.strip()
                            case 2:
                                texto_analise_2 = ' '.join([texto_analise_2, line.strip()])
                                dicionario[key_atendimento]['texto2'] = texto_analise_2.strip()
                            case 3:
                                texto_analise_3 = ' '.join([texto_analise_3, line.strip()])
                                dicionario[key_atendimento]['texto3'] = texto_analise_3.strip()

                        valor_copart = extract_value(texto_analise, texto_analise_2, texto_analise_3)

                        if valor_copart[0] or valor_copart[1]:
                            dicionario[key_atendimento]['decote'] = valor_copart[0]  # type: ignore
                            dicionario[key_atendimento]['resto'] = valor_copart[1]  # type: ignore

    return dicionario
