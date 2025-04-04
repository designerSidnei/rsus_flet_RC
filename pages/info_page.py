"""
Módulo que implementa a página de informações do aplicativo RSUS.

Este módulo contém a implementação da página que exibe informações
sobre o aplicativo, como versão, desenvolvedor e datas importantes.
"""

from flet import (
    FontWeight,
    MainAxisAlignment,
    Row,
    TextAlign,
    Page,
    Text,
    CrossAxisAlignment,
    Column,
    Container,
)

import json


class Info(Column):
    """
    Página de informações do aplicativo.

    Esta classe implementa a interface que exibe informações gerais sobre
    o aplicativo, incluindo:
    - Nome e descrição do aplicativo
    - Desenvolvedor
    - Data de criação
    - Versão atual
    - Data da última atualização

    As informações são carregadas de um arquivo JSON de configuração.

    Args:
        page (Page): Página principal do aplicativo Flet
    """

    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.visible = False
        self.text: dict[str, str] = {}

        # Carregar o arquivo de informações
        with open("./dados/info.json", "r", encoding="utf-8") as j:
            self.text = json.load(j)

        # Construir o layout de informações
        info_layout = Container(
            expand=True,
            content=Column(
                expand=True,
                controls=[
                    Text(
                        self.text["Info"],
                        size=30,
                        weight=FontWeight.BOLD,
                        text_align=TextAlign.CENTER,
                    ),
                    Text(
                        self.text["Rsus"],
                        size=20,
                        weight=FontWeight.BOLD,
                        text_align=TextAlign.CENTER,
                    ),
                    Row(
                        expand=True,
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            Column(
                                horizontal_alignment=CrossAxisAlignment.END,
                                controls=[
                                    Text(
                                        "Desenvolvedor:",
                                        size=15,
                                        italic=True,
                                        weight=FontWeight.BOLD,
                                        text_align=TextAlign.CENTER,
                                    ),
                                    Text(
                                        "Data de criação:",
                                        size=15,
                                        italic=True,
                                        weight=FontWeight.BOLD,
                                        text_align=TextAlign.CENTER,
                                    ),
                                    Text(
                                        "Versão:",
                                        size=15,
                                        italic=True,
                                        weight=FontWeight.BOLD,
                                        text_align=TextAlign.CENTER,
                                    ),
                                    Text(
                                        "Última atualização:",
                                        size=15,
                                        italic=True,
                                        weight=FontWeight.BOLD,
                                        text_align=TextAlign.RIGHT,
                                    ),
                                ],
                            ),
                            Column(
                                horizontal_alignment=CrossAxisAlignment.START,
                                controls=[
                                    Text(
                                        self.text["Desenvolvedor"],
                                        size=15,
                                        italic=True,
                                        text_align=TextAlign.CENTER,
                                    ),
                                    Text(
                                        self.text["Data"],
                                        size=15,
                                        italic=True,
                                        text_align=TextAlign.CENTER,
                                    ),
                                    Text(
                                        self.text["Versão"],
                                        size=15,
                                        italic=True,
                                        text_align=TextAlign.CENTER,
                                    ),
                                    Text(
                                        self.text["Atualização"],
                                        size=15,
                                        italic=True,
                                        text_align=TextAlign.LEFT,
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
                horizontal_alignment=CrossAxisAlignment.CENTER,
            ),
        )

        # Construir o conteúdo principal
        self.content = Column(
            expand=True,
            # width=660,
            width=self.page.window.width - 135,
            horizontal_alignment=CrossAxisAlignment.CENTER,
            controls=[info_layout],
        )

        # Adicionar o conteúdo como controle do Column
        self.controls = [self.content]
        self.expand = True
        # self.alignment = MainAxisAlignment.CENTER
