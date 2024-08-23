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
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.visible = False
        self.progress_bar = ProgressBar()
        self.plan = CustomTextField("Planilha com base para memória")
        self.plan_button = Buttons("Buscar", icons.SEARCH, self.plan, ["xlsx"])

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

    def build(self):
        return Container(
            expand=True,
            content=Column(
                expand=True,
                alignment="center",
                spacing=0,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[self.plan_path, self.do_it_button],
            ),
        )

    async def memo(self, planilha_path):
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
        dlg.open = False
        self.page.update()
