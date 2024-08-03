from flet import (
    Page, ProgressBar, AlertDialog, Text, TextButton, Container,
    Column, Row, ElevatedButton, MainAxisAlignment, alignment, icons
)

from components.buttons import DirButton
from components.text_fields import CustomTextField

from pathlib import Path

from modules.move_form import copy_pdf_to_folder

import asyncio


class MoverPDF(Row):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page

        self.progress_bar = ProgressBar()
        self.dlg = AlertDialog(
            modal=True,
            title=Text("Aguarde..."),
            content=self.progress_bar,
            actions=[TextButton("OK", on_click=self.close_dlg)],
            actions_alignment=MainAxisAlignment.CENTER,
        )

        self.sorce_dir = CustomTextField("Diretório de origem")
        self.target_dir = CustomTextField("Diretório de destino")
        self.source_button = DirButton("Buscar", icons.SEARCH, self.sorce_dir)
        self.target_button = DirButton("Buscar", icons.SEARCH, self.target_dir)

        self.folder_dir = Container(expand=1, alignment=alignment.top_center,
                                    content=Column(
                                        expand=True,
                                        alignment="center",
                                        controls=[
                                            Row(expand=True, alignment="center", controls=[
                                                self.sorce_dir,
                                                self.source_button,
                                            ]),
                                            Row(expand=True, alignment="center", controls=[
                                                self.target_dir,
                                                self.target_button
                                            ]),
                                        ]
                                    ))

    def build(self):
        return Container(expand=True,
                         width=self.page.window_width,
                         alignment=alignment.center,
                         content=Column(
                             expand=True,
                             alignment="center",
                             spacing=0,
                             controls=[
                                 self.folder_dir,
                                 Row(expand=1, alignment="center", controls=[
                                     ElevatedButton("Executar", icons.RUN_CIRCLE, height=50, width=170,
                                                    on_click=lambda _: asyncio.run(self.move_pdfs(self.source_button.path_name, self.target_button.path_name)))
                                     ])
                             ]
                         ))

    def close_dlg(self, e):
        self.dlg.open = False
        self.page.update()

    async def move_pdfs(self, source_dir, target_dir):
        self.page.dialog = self.dlg
        self.dlg.open = True
        self.page.update()

        source_dir_path = Path(source_dir)
        target_dir_path = Path(target_dir)

        move_files = asyncio.create_task(copy_pdf_to_folder(source_dir_path, target_dir_path))
        result = await move_files

        if result:
            self.dlg.title = Text("Resultado:")
            self.dlg.content = Text(result)
            self.page.update()

