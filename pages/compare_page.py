"""
Módulo que implementa a página de comparação (batimento) de dados do aplicativo RSUS.

Este módulo contém a implementação da página que permite ao usuário
comparar duas listas de dados de uma planilha, identificando valores
que existem em uma lista mas não na outra.
"""

from flet import (
    Page,
    Container,
    ElevatedButton,
    Row,
    Column,
    alignment,
    DataTable,
    DataColumn,
    icons,
    DataRow,
    DataCell,
    Text,
    AlertDialog,
    TextButton,
    MainAxisAlignment,
)

import pandas as pd
import pyperclip as pc

from components.buttons import Buttons
from components.text_fields import CustomTextField


class Batimento(Row):
    """
    Página de comparação (batimento) de dados.

    Esta classe implementa a interface para comparar duas listas de dados,
    permitindo ao usuário:
    - Carregar uma planilha com duas colunas de dados
    - Visualizar os dados em uma tabela comparativa
    - Identificar valores que existem em uma lista mas não na outra
    - Copiar os resultados para a área de transferência

    Args:
        page (Page): Página principal do aplicativo Flet
    """

    def __init__(self, page: Page):
        super().__init__()
        self.page = page

        self.plan_text_field = CustomTextField("Planilha para batimento")
        self.plan_button = Buttons(
            page, "Buscar", icons.SEARCH, self.plan_text_field, ["xlsx"]
        )

        self.dlg = AlertDialog(
            modal=True,
            actions=[TextButton("OK", on_click=self.close_dlg)],
            actions_alignment=MainAxisAlignment.CENTER,
        )

        self.header = [self.tit("Lista 1"), self.tit("Lista 2"), self.tit("Resultado")]
        self.matriz = [
            ["", "", ""],
            ["", "", ""],
            ["", "", ""],
            ["", "", ""],
        ]
        self.body = self.cel(self.matriz)

        self.plan_path = Container(
            expand=1,
            alignment=alignment.center,
            content=Row(
                expand=True,
                alignment="center",
                controls=[
                    self.plan_text_field,
                    Column(
                        controls=[
                            self.plan_button,
                            ElevatedButton(
                                "Executar",
                                icons.RUN_CIRCLE_OUTLINED,
                                width=140,
                                on_click=lambda _: self.list_dict(
                                    self.plan_button.path_name
                                ),
                            ),
                        ]
                    ),
                ],
            ),
        )

        self.dt_table = DataTable(columns=self.header, rows=self.body, width=500)
        self.batimento_data = Container(
            expand=2,
            alignment=alignment.center,
            content=Column(
                expand=True,
                scroll=True,
                controls=[self.dt_table],
            ),
        )

        # Construir o conteúdo principal
        self.content = Container(
            expand=True,
            # width=self.page.window.width,
            width=self.page.window.width - 135,
            alignment=alignment.center,
            padding=10,
            content=Column(
                expand=True,
                alignment="center",
                controls=[self.plan_path, self.batimento_data],
            ),
        )

        # Adicionar o conteúdo como controle do Row
        self.controls = [self.content]
        self.expand = True
        # self.alignment = MainAxisAlignment.CENTER

    def close_dlg(self, e):
        """
        Fecha o diálogo de informação.

        Args:
            e: Evento do botão de fechar
        """
        self.dlg.open = False
        self.page.update()

    def tit(self, texto):
        """
        Cria uma coluna de título para a tabela de dados.

        Args:
            texto (str): Texto do título da coluna

        Returns:
            DataColumn: Coluna formatada para a tabela
        """
        return DataColumn(Text(texto))

    def cel(self, matriz):
        """
        Converte uma matriz de dados em linhas para a tabela.

        Args:
            matriz (list): Lista de listas contendo os dados para a tabela

        Returns:
            list: Lista de DataRow formatados para a tabela
        """
        linhas = []
        i = 0
        for linha in matriz:
            i += 1
            celulas = []
            for celula in linha:
                celulas.append(DataCell(Text(celula)))
            linhas.append(DataRow(cells=celulas))
        return linhas

    def list_dict(self, plan):
        """
        Processa a planilha e realiza o batimento dos dados.

        Este método:
        - Carrega as duas colunas da planilha
        - Compara os valores entre as listas
        - Identifica valores únicos em cada lista
        - Atualiza a tabela com os resultados
        - Copia os valores diferentes para a área de transferência

        Args:
            plan (str): Caminho do arquivo da planilha
        """
        df = pd.read_excel(plan, sheet_name=0, header=None)
        matriz = []

        # Passa a primeira e segunda coluna para lista
        lista_a = df[0].tolist()
        lista_a = [x for x in lista_a if pd.notna(x)]

        lista_b = df[1].tolist()
        lista_b = [x for x in lista_b if pd.notna(x)]

        # Verifica e retorna os valores que tem em uma lista e não tem na outra
        def nao_tem_na_lista(lista_um, lista_dois):
            nao_tem_na_lista_dois = [
                str(lista_um[n])
                for n in range(0, len(lista_um))
                if lista_um[n] not in lista_dois
            ]
            return nao_tem_na_lista_dois

        primeira_lista = nao_tem_na_lista(lista_a, lista_b)
        segunda_lista = nao_tem_na_lista(lista_b, lista_a)
        # Junta os valores que não tem nas listas
        terceira_lista = primeira_lista + segunda_lista

        len_lista = max(len(lista_a), len(lista_b), len(terceira_lista))

        for l in range(len_lista):
            lista_ = [
                lista_a[l] if l < len(lista_a) else "",
                lista_b[l] if l < len(lista_b) else "",
                terceira_lista[l] if l < len(terceira_lista) else "",
            ]
            matriz.append(lista_)

        # Copia os valores que não batem para o clipboard
        pc.copy("\n".join(terceira_lista))

        self.body = self.cel(matriz)
        self.dt_table.rows = self.body
        self.dt_table.update()

        self.page.dialog = self.dlg
        self.dlg.open = True
        self.dlg.title = Text("Info:")
        self.dlg.content = Text(
            "O resultado da operação foi copiado para a área de transferência."
        )

        self.page.update()
