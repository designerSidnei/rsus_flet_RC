from flet import (
    Page, Container, Row, Column, MainAxisAlignment, alignment, icons,
    ElevatedButton, AlertDialog, Text, TextButton, ProgressBar
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
        self.dlg = AlertDialog(
            modal=True,
            title=Text("Aguarde..."),
            content=self.progress_bar,
            actions=[TextButton("OK", on_click=self.close_dlg)],
            actions_alignment=MainAxisAlignment.CENTER,
        )

        self.plan = CustomTextField("Planilha de base para abertura de pastas")
        self.plan_button = Buttons("Buscar", icons.SEARCH, self.plan, ["xlsx"])
        
        self.plan_path = Container(
            expand=1,
            alignment=alignment.center,
            content=Row(expand=True, alignment=MainAxisAlignment.CENTER,
                        controls=[self.plan,
                                  self.plan_button])
        )
    
    def build(self):
        return Container(
            expand=True,
            width=self.page.window_width,
            alignment=alignment.top_center,
            content=(
                Column(
                    expand=True,
                    alignment="center",
                    spacing=0,
                    controls=[self.plan_path,
                              Row(expand=1, alignment=MainAxisAlignment.CENTER,
                                  controls=[
                                      ElevatedButton("Executar", width=140, height=50,
                                                     on_click=lambda _: asyncio.run(self.open_folder(self.plan_button.path_name)))
                                      ])]
                )
            )
        )
    
    def close_dlg(self, e):
        self.dlg.open = False
        self.page.update()
    
    async def open_folder(self, plan_path):

        self.page.dialog = self.dlg
        self.dlg.open = True
        self.page.update()

        abrir_pastas_ = asyncio.create_task(abrir_pastas(plan_path))
        result = await abrir_pastas_
        
        if result:
            self.dlg.title = Text("Resultado:")
            self.dlg.content = Text(result)
            self.page.update()
