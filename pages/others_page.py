from flet import (
    Page,
    Row,
    Tabs, Tab,
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

        self.tab = Tabs(
            tabs=[self.compare_page, self.open_page, self.move_pdf_page],
            selected_index=0,
            width=self.page.window_width - 130
        )
    
    def build(self):
        return self.tab
    
