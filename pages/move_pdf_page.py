"""
Módulo que implementa a página de movimentação de PDFs do aplicativo RSUS.

Este módulo contém a implementação da página que permite ao usuário
mover arquivos PDF entre diretórios do sistema, facilitando a
organização dos documentos.
"""

from flet import (
    Page,
    ProgressBar,
    AlertDialog,
    Text,
    TextButton,
    Container,
    Column,
    Row,
    ElevatedButton,
    MainAxisAlignment,
    alignment,
    icons,
)

from components.buttons import DirButton
from components.text_fields import CustomTextField

from pathlib import Path

from modules.move_form import copy_pdf_to_folder

import asyncio


class MoverPDF(Row):
    """
    Página de movimentação de arquivos PDF.

    Esta classe implementa a interface para mover arquivos PDF entre
    diretórios, permitindo ao usuário:
    - Selecionar um diretório de origem
    - Selecionar um diretório de destino
    - Mover todos os PDFs da origem para o destino
    - Visualizar o progresso e resultado da operação

    Args:
        page (Page): Página principal do aplicativo Flet
    """

    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.progress_bar = ProgressBar()
        self.sorce_dir = CustomTextField("Diretório de origem")
        self.target_dir = CustomTextField("Diretório de destino")
        self.source_button = DirButton(page, "Buscar", icons.SEARCH, self.sorce_dir)
        self.target_button = DirButton(page, "Buscar", icons.SEARCH, self.target_dir)

        self.folder_dir = Container(
            expand=1,
            alignment=alignment.top_center,
            content=Column(
                expand=True,
                alignment="center",
                controls=[
                    Row(
                        expand=True,
                        alignment="center",
                        controls=[
                            self.sorce_dir,
                            self.source_button,
                        ],
                    ),
                    Row(
                        expand=True,
                        alignment="center",
                        controls=[self.target_dir, self.target_button],
                    ),
                ],
            ),
        )

        # Construir o conteúdo principal
        self.content = Container(
            expand=True,
            # width=self.page.window.width,
            width=self.page.window.width - 135,
            alignment=alignment.center,
            content=Column(
                expand=True,
                alignment="center",
                spacing=0,
                controls=[
                    self.folder_dir,
                    Row(
                        expand=1,
                        alignment="center",
                        controls=[
                            ElevatedButton(
                                "Executar",
                                icons.RUN_CIRCLE,
                                height=50,
                                width=170,
                                on_click=lambda _: asyncio.run(
                                    self.move_pdfs(
                                        self.source_button.path_name,
                                        self.target_button.path_name,
                                    )
                                ),
                            )
                        ],
                    ),
                ],
            ),
        )

        # Adicionar o conteúdo como controle do Row
        self.controls = [self.content]
        self.expand = True
        # self.alignment = MainAxisAlignment.CENTER

    def close_dlg(self, dlg):
        """
        Fecha o diálogo de progresso/resultado.

        Args:
            dlg (AlertDialog): Diálogo a ser fechado
        """
        dlg.open = False
        self.page.update()

    async def move_pdfs(self, source_dir, target_dir):
        """
        Executa a movimentação dos arquivos PDF de forma assíncrona.

        Este método copia todos os arquivos PDF do diretório de origem
        para o diretório de destino, exibindo o progresso e resultado
        em um diálogo.

        Args:
            source_dir (str): Caminho do diretório de origem
            target_dir (str): Caminho do diretório de destino
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

        source_dir_path = Path(source_dir)
        target_dir_path = Path(target_dir)

        move_files = asyncio.create_task(
            copy_pdf_to_folder(source_dir_path, target_dir_path)
        )
        result = await move_files

        if result:
            dlg.title = Text("Resultado:")
            dlg.content = Text(result)
            self.page.update()
