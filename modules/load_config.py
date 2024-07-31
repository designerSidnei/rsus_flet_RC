import json


def config_read():
    """Lê o arquivo de configuração e retorna seu conteúdo como um dicionário Python.

    Return:
        Um dicionário Python contendo os dados de configuração.
    """
    with open('./dados/config.json', 'r', encoding='utf-8') as j:
        return json.load(j)
