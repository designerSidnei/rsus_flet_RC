"""
Módulo que implementa a página de renomeação de arquivos do aplicativo RSUS.

Este módulo contém a implementação da página que permite ao usuário
selecionar múltiplos arquivos PDF e renomeá-los de acordo com dados
de uma planilha.
"""

from flet import (
    Page,
    FilePicker,
    icons,
    Row,
    Column,
    ListView,
    ElevatedButton,
    Container,
    border,
    alignment,
    MainAxisAlignment,
    CrossAxisAlignment,
    Text,
    FilePickerResultEvent,
)

from components.buttons import Buttons
from components.text_fields import CustomTextField

import asyncio

from modules.renomeia import caminho_arquivos


class Rename(Row):
    """
    Página de renomeação de arquivos.

    Esta classe implementa a interface para renomear múltiplos arquivos PDF,
    permitindo ao usuário selecionar uma planilha com os novos nomes e os
    arquivos a serem renomeados.

    Args:
        page (Page): Página principal do aplicativo Flet
    """

    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.visible = False
        self.pick_files = FilePicker(on_result=self.pick_files_result)
        self.list_files = []
        self.list_path_files = []
        self.page.overlay.append(self.pick_files)
        self.arquivos = CustomTextField(hint="Planilha com dados para renomear docs")
        self.plan_button = Buttons(
            page, "Buscar dados", icons.SEARCH, self.arquivos, ["xlsx"]
        )

        # Construir os componentes
        self.texts_field_um = Row(
            alignment=MainAxisAlignment.CENTER,
            controls=[
                self.arquivos,
                self.plan_button,
            ],
        )

        self.list_view_files = ListView(
            expand=True, spacing=5, padding=10, divider_thickness=1
        )

        self.texts_field_dois = Column(
            alignment="center",
            expand=True,
            controls=[
                ElevatedButton(
                    "Buscar docs",
                    icon=icons.SEARCH,
                    height=50,
                    width=140,
                    on_click=lambda _: self.pick_files.pick_files(
                        allow_multiple=True, allowed_extensions=["pdf"]
                    ),
                ),
                Container(
                    expand=True,
                    border=border.all(1, "Black"),
                    width=500,
                    alignment=alignment.center,
                    content=self.list_view_files,
                ),
            ],
        )

        # Construir o conteúdo principal
        self.content = Column(
            horizontal_alignment=CrossAxisAlignment.CENTER,
            spacing=0,
            width=self.page.window.width - 135,
            controls=[
                Container(
                    expand=1,
                    content=self.texts_field_um,
                ),
                Container(expand=3, content=self.texts_field_dois),
                Container(
                    expand=1,
                    alignment=alignment.center,
                    content=ElevatedButton(
                        "Renomear",
                        icons.EDIT_DOCUMENT,
                        height=50,
                        width=140,
                        on_click=lambda _: asyncio.run(
                            self.rename(
                                self.plan_button.path_name, self.list_path_files
                            )
                        ),
                    ),
                ),
            ],
        )

        # Adicionar o conteúdo como controle do Row
        self.controls = [self.content]
        self.expand = True
        # self.alignment = MainAxisAlignment.CENTER

    def pick_files_result(self, e: FilePickerResultEvent):
        """
        Manipula o resultado da seleção de arquivos.

        Este método é chamado quando o usuário seleciona arquivos através
        do FilePicker. Atualiza a lista de arquivos selecionados na interface.

        Args:
            e (FilePickerResultEvent): Evento contendo os arquivos selecionados
        """
        selected_files = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelado!"
        )
        selected_path_files = (
            ", ".join(map(lambda f: f.path, e.files)) if e.files else "Cancelado!"
        )

        self.list_files = selected_files.split(",")
        self.list_path_files = selected_path_files.split(",")

        if self.list_files:
            if len(self.list_view_files.controls) > 0:
                self.list_view_files.clean()                

            for item in self.list_files:
                self.list_view_files.controls.append(Text(item))
            self.list_view_files.update()

    async def rename(self, plan_path, arquivos):
        """
        Executa a renomeação dos arquivos de forma assíncrona.

        Este método processa a renomeação dos arquivos selecionados usando
        os dados da planilha especificada e atualiza a interface com o resultado.

        Args:
            plan_path (str): Caminho do arquivo da planilha com os novos nomes
            arquivos (list): Lista de caminhos dos arquivos a serem renomeados
        """
        renomeia = asyncio.create_task(caminho_arquivos(plan_path, arquivos))
        result = await renomeia
        if result:
            self.list_view_files.clean()
            for item in result:
                self.list_view_files.controls.append(Text(item))
            self.list_view_files.update()
