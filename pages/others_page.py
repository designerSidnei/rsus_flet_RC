"""
Módulo que implementa a página de outras funcionalidades do aplicativo RSUS.

Este módulo contém a implementação da página que agrupa funcionalidades
adicionais do aplicativo em abas separadas, incluindo:
- Batimento de dados
- Abertura de pastas
- Movimentação de PDFs
"""

from flet import (
    Page,
    Row,
    Tabs,
    Tab,
)
from pages.compare_page import Batimento
from pages.open_folder_page import AbrirPasta
from pages.move_pdf_page import MoverPDF


class Outros(Row):
    """
    Página de funcionalidades adicionais.

    Esta classe implementa uma interface com abas que agrupa diferentes
    funcionalidades auxiliares do aplicativo:
    - Batimento: Comparação de dados entre planilhas
    - Abrir pasta: Acesso rápido a diretórios do sistema
    - Mover PDF: Organização de arquivos PDF

    Args:
        page (Page): Página principal do aplicativo Flet
    """

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
