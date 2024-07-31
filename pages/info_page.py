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
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.visible = False
        self.text: dict[str, str] = {}

    def build(self):
        with open("./dados/info.json", "r", encoding="utf-8") as j:
            self.text = json.load(j)

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

        return Column(
            expand=True,
            width=660,
            horizontal_alignment=CrossAxisAlignment.CENTER,
            controls=[info_layout],
        )
