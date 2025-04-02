from flet import (
    Page,
    Row,
    Tabs,
    Tab,
    MainAxisAlignment,
)
from pages.compare_page import Batimento
from pages.open_folder_page import AbrirPasta
from pages.move_pdf_page import MoverPDF


class Outros(Row):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.visible = False
        self.compare_page = Tab(text="Batimento", content=Batimento(page))
        self.open_page = Tab(text="Abrir pasta", content=AbrirPasta(page))
        self.move_pdf_page = Tab(text="Mover PDF", content=MoverPDF(page))

        # Construir o conteúdo principal
        self.content = Tabs(
            tabs=[self.compare_page, self.open_page, self.move_pdf_page],
            selected_index=0,
            width=self.page.window.width - 135,
        )

        # Adicionar o conteúdo como controle do Row
        self.controls = [self.content]
        self.expand = True
        # self.alignment = MainAxisAlignment.CENTER
