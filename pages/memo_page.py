"""
Módulo que implementa a página de memória de cálculo do aplicativo RSUS.

Este módulo contém a implementação da página que permite ao usuário
processar planilhas para gerar memórias de cálculo automaticamente.
"""

from flet import (
    Page,
    ProgressBar,
    AlertDialog,
    Text,
    TextButton,
    ElevatedButton,
    Container,
    Column,
    Row,
    MainAxisAlignment,
    CrossAxisAlignment,
    icons,
    alignment,
)
from components.buttons import Buttons
from components.text_fields import CustomTextField

import pandas as pd

import asyncio

from modules.memoria_de_calculo import process_rows


class Memo(Column):
    """
    Página de geração de memória de cálculo.

    Esta classe implementa a interface para processar planilhas e gerar
    memórias de cálculo automaticamente, permitindo ao usuário selecionar
    uma planilha base para o processamento.

    Args:
        page (Page): Página principal do aplicativo Flet
    """

    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.visible = False
        self.progress_bar = ProgressBar()
        self.plan = CustomTextField("Planilha com base para memória")
        self.plan_button = Buttons(page, "Buscar", icons.SEARCH, self.plan, ["xlsx"])

        self.plan_path = Container(
            expand=1,
            alignment=alignment.top_center,
            content=Row(
                expand=True,
                alignment=MainAxisAlignment.CENTER,
                controls=[self.plan, self.plan_button],
            ),
        )
        self.do_it_button = Container(
            expand=1,
            alignment=alignment.top_center,
            content=ElevatedButton(
                "Executar",
                icons.RUN_CIRCLE,
                height=50,
                width=140,
                on_click=lambda _: asyncio.run(self.memo(self.plan_button.path_name)),
            ),
        )

        # Construir o conteúdo principal
        self.content = Container(
            expand=True,
            content=Column(
                expand=True,
                alignment="center",
                width=self.page.window.width - 135,
                spacing=0,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[self.plan_path, self.do_it_button],
            ),
        )

        # Adicionar o conteúdo como controle do Column
        self.controls = [self.content]
        self.expand = True
        # self.alignment = MainAxisAlignment.CENTER

    async def memo(self, planilha_path):
        """
        Processa a planilha para gerar a memória de cálculo.

        Este método executa o processamento da planilha de forma assíncrona
        e exibe o progresso e resultado em um diálogo.

        Args:
            planilha_path (str): Caminho do arquivo da planilha base
        """
        dlg = AlertDialog(
            modal=True,
            title=Text("Aguarde..."),
            content=self.progress_bar,
            actions=[TextButton("OK", on_click=lambda _: self.close_dlg(dlg))],
            actions_alignment=MainAxisAlignment.CENTER,
        )
        self.page.overlay.append(dlg)
        dlg.open = True
        self.page.update()

        df = pd.read_excel(planilha_path)
        memor = asyncio.create_task(process_rows(df, planilha_path))
        result = await memor

        if result:
            dlg.title = Text("Resultado:")
            dlg.content = Text(result)
            self.page.update()

    def close_dlg(self, dlg):
        """
        Fecha o diálogo de progresso/resultado.

        Args:
            dlg (AlertDialog): Diálogo a ser fechado
        """
        dlg.open = False
        self.page.update()
