from flet import (
    Page,
    Container,
    Row,
    Column,
    MainAxisAlignment,
    alignment,
    icons,
    ElevatedButton,
    AlertDialog,
    Text,
    TextButton,
    ProgressBar,
)

from components.buttons import Buttons
from components.text_fields import CustomTextField

import asyncio

from modules.open_files import abrir_pastas


class AbrirPasta(Row):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.progress_bar = ProgressBar()
        self.plan = CustomTextField("Planilha de base para abertura de pastas")
        self.plan_button = Buttons("Buscar", icons.SEARCH, self.plan, ["xlsx"])

        self.plan_path = Container(
            expand=1,
            alignment=alignment.center,
            content=Row(
                expand=True,
                alignment=MainAxisAlignment.CENTER,
                controls=[self.plan, self.plan_button],
            ),
        )

        # Construir o conteúdo principal
        self.content = Container(
            expand=True,
            # width=self.page.window.width,
            width=self.page.window.width - 135,
            alignment=alignment.top_center,
            content=Column(
                expand=True,
                alignment="center",
                spacing=0,
                controls=[
                    self.plan_path,
                    Row(
                        expand=1,
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            ElevatedButton(
                                "Executar",
                                icons.RUN_CIRCLE,
                                width=140,
                                height=50,
                                on_click=lambda _: asyncio.run(
                                    self.open_folder(self.plan_button.path_name)
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
        dlg.open = False
        self.page.update()

    async def open_folder(self, plan_path):
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
        result = None

        abrir_pastas_ = asyncio.create_task(abrir_pastas(plan_path))
        if not abrir_pastas_.done():
            result = await abrir_pastas_

        if result:
            dlg.title = Text("Resultado:")
            dlg.content = Text(result)
            self.page.update()