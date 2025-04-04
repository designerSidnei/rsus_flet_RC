"""
Módulo que implementa a página de processamento de decisões do aplicativo RSUS.

Este módulo contém a implementação da página que permite ao usuário
processar decisões a partir de planilhas e notas técnicas.
"""

from flet import (
    Page,
    AlertDialog,
    ProgressBar,
    Text,
    TextButton,
    MainAxisAlignment,
    CrossAxisAlignment,
    icons,
    Column,
    Row,
    Container,
    ElevatedButton,
)

from components.buttons import Buttons
from components.text_fields import CustomTextField

import asyncio

from modules.decisoes import mainn


class Decisao(Row):
    """
    Página de processamento de decisões.

    Esta classe implementa a interface para processar decisões, permitindo
    ao usuário selecionar uma planilha de decisão e uma nota técnica
    para processamento.

    Args:
        page (Page): Página principal do aplicativo Flet
    """

    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.progress_bar = ProgressBar()
        self.planilha = CustomTextField("Planilha da decisão")
        self.dados = CustomTextField("Nota técnica")
        self.plan_path = None
        self.plan_dados = None
        self.plan_button = Buttons(
            page, "Buscar planilha", icons.FILE_OPEN_OUTLINED, self.planilha, ["xlsx"]
        )
        self.dados_button = Buttons(
            page, "Buscar dados", icons.FILE_OPEN_OUTLINED, self.dados, ["pdf"]
        )
        self.visible = False

        # Construir o conteúdo principal
        self.content = Column(
            controls=[
                Row(
                    controls=[self.planilha, self.plan_button],
                    alignment="center",
                ),
                Row(
                    controls=[self.dados, self.dados_button],
                    alignment="center",
                ),
                ElevatedButton(
                    text="Executar",
                    height=50,
                    icon=icons.RUN_CIRCLE,
                    on_click=lambda _: asyncio.run(
                        self.passar_decisao(
                            self.plan_button.path_name, self.dados_button.path_name
                        )
                    ),
                ),
            ],
            # expand=True,
            width=self.page.window.width - 135,
            horizontal_alignment=CrossAxisAlignment.CENTER,
        )

        # Adicionar o conteúdo como controle do Row
        self.controls = [self.content]
        # self.expand = True
        # self.alignment = MainAxisAlignment.CENTER

    def close_dlg(self, dlg):
        """
        Fecha o diálogo de progresso/resultado.

        Args:
            dlg (AlertDialog): Diálogo a ser fechado
        """
        dlg.open = False
        self.page.update()

    async def passar_decisao(self, plan_path, plan_dados):
        """
        Processa a decisão de forma assíncrona.

        Este método executa o processamento da decisão usando os arquivos
        selecionados pelo usuário e exibe o progresso e resultado em um diálogo.

        Args:
            plan_path (str): Caminho do arquivo da planilha
            plan_dados (str): Caminho do arquivo da nota técnica

        Returns:
            None
        """
        try:
            self.plan_path = plan_path
            self.plan_dados = plan_dados

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

            result = await asyncio.create_task(mainn(self.plan_path, self.plan_dados)) # quando é retornado algum valor é obrigatório o uso de 'await'

            dlg.title = Text("Resultado:")
            dlg.content = Text(result) if result else Text("Nenhuma resultado encontrado.")
            self.page.update()
        except Exception as e:
            dlg.title = Text("Erro:")
            dlg.content = Text(f"Ocorreu um erro: {str(e)}.")
            self.page.update()
