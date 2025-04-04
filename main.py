"""
RSUS - Aplicativo para auxiliar no processamento de documentos do SUS.

Este módulo contém a implementação principal do aplicativo RSUS, incluindo
a interface gráfica e a lógica de navegação entre páginas.
"""

import json
from pathlib import Path
from flet import (
    Page,
    app,
    Theme,
    ColorScheme,
    AppBar,
    NavigationRailDestination,
    NavigationRailLabelType,
    NavigationRail,
    Text,
    TextField,
    ElevatedButton,
    Container,
    Column,
    Row,
    MainAxisAlignment,
    IconButton,
    AlertDialog,
    margin,
    padding,
    Icons,
    Colors,
    SnackBar,
)

from pages.main_page import MainPage
from pages.decision_page import Decisao
from pages.rename_page import Rename
from pages.memo_page import Memo
from pages.others_page import Outros
from pages.settings_page import Config
from pages.info_page import Info

# from modules.load_config import config_read

# config = config_read()


class SideBar(Row):
    """
    Barra de navegação lateral do aplicativo.

    Esta classe implementa a barra de navegação lateral que permite
    alternar entre as diferentes páginas do aplicativo.

    Args:
        page (Page): Página principal do aplicativo
        main_page (Row): Página inicial
        decision (Row): Página de decisão
        rename (Row): Página de renomeação
        memo (Column): Página de memória de cálculo
        other (Row): Página de outras opções
        info (Column): Página de informações
        settings (Column): Página de configurações
    """

    def __init__(
        self,
        page: Page,
        main_page: Row,
        decision: Row,
        rename: Row,
        memo: Column,
        other: Row,
        info: Column,
        settings: Column,
    ):
        super().__init__()
        self.page = page
        self.main_page = main_page
        self.decision = decision
        self.rename = rename
        self.memo = memo
        self.other = other
        self.settings = settings
        self.info = info

        self.nav_itens = [
            NavigationRailDestination(
                label_content=Text("Página inicial"),
                label="Página inicial",
                icon=Icons.HOME,
                selected_icon=Icons.HOME_OUTLINED,
            ),
            NavigationRailDestination(
                label_content=Text("Decisão"),
                label="Decisão",
                icon=Icons.ACCESS_TIME_FILLED,
                selected_icon=Icons.ACCESS_TIME_OUTLINED,
            ),
            NavigationRailDestination(
                label_content=Text("Renomear"),
                label="Renomear",
                icon=Icons.EDIT,
                selected_icon=Icons.EDIT_OUTLINED,
            ),
            NavigationRailDestination(
                label_content=Text("Memória"),
                label="Memória",
                icon=Icons.NUMBERS,
                selected_icon=Icons.NUMBERS_OUTLINED,
            ),
            NavigationRailDestination(
                label_content=Text("Outros"),
                label="Outros",
                icon=Icons.MORE,
                selected_icon=Icons.MORE_OUTLINED,
            ),
        ]

        self.nav_rail = NavigationRail(
            selected_index=0,
            expand=True,
            label_type=NavigationRailLabelType.ALL,
            on_change=self.mudar_pagina,
            destinations=self.nav_itens,
            bgcolor=Colors.BLACK12,
            height=310,
        )

        # Construir a view imediatamente
        self.view = Container(
            content=Column(
                controls=[
                    self.nav_rail,
                ],
                expand=True,
            ),
            padding=0,
            margin=margin.all(0),
            width=120,
        )
        
        # Adicionar a view como conteúdo do Row
        self.controls = [self.view]
        self.expand = True

    def set_app_main_bar_pages(self, index):
        """
        Define qual página deve estar visível com base no índice selecionado.

        Args:
            index (int): Índice da página a ser exibida
        """
        pages_list = [
            self.main_page,
            self.decision,
            self.rename,
            self.memo,
            self.other,
            self.settings,
            self.info,
        ]
        for page in pages_list:
            page.visible = False
        pages_list[index].visible = True

    def mudar_pagina(self, e):
        """
        Manipula a mudança de páginas quando um item da navegação é selecionado.

        Args:
            e: Evento de mudança de página ou índice da página
        """
        index = e if isinstance(e, int) else e.control.selected_index

        if index == 0:
            self.page.appbar.title = Text("Página inicial")
            self.set_app_main_bar_pages(index)
        elif index == 1:
            self.page.appbar.title = Text("Decisão")
            self.set_app_main_bar_pages(index)
        elif index == 2:
            self.page.appbar.title = Text("Renomear")
            self.set_app_main_bar_pages(index)
        elif index == 3:
            self.page.appbar.title = Text("Memória de cálculo")
            self.set_app_main_bar_pages(index)
        elif index == 4:
            self.page.appbar.title = Text("Outras opções")
            self.set_app_main_bar_pages(index)
        self.page.update()


def main(page: Page):
    """
    Função principal do aplicativo.

    Configura e inicializa a interface do usuário, incluindo:
    - Configuração da janela principal
    - Inicialização das páginas
    - Configuração da barra de navegação
    - Gerenciamento das configurações do usuário

    Args:
        page (Page): Página principal do aplicativo Flet
    """
    page.title = "RSUS"
    page.window.width = 800
    page.window.height = 520
    page.window.maximizable = False
    page.window.resizable = False
    page.window.center()
    page.padding = 0
    page.bgcolor = Colors.BLUE_GREY_900

    page.theme = Theme(
        color_scheme=ColorScheme(
            primary=Colors.BLUE_400,
            # secondary_container=Colors.BLUE_400
        ),
        color_scheme_seed=Colors.BLUE,
    )

    # Inicialização das páginas
    main_page = MainPage(page)
    decision_page = Decisao(page)
    rename_page = Rename(page)
    memo_page = Memo(page)
    others_page = Outros(page)
    info_page = Info(page)
    settings_page = Config(page)

    all_pages = [
        main_page,
        decision_page,
        rename_page,
        memo_page,
        others_page,
        info_page,
        settings_page
    ]

    def set_app_bar_pages(current_page: Row):
        for each_page in all_pages:
            each_page.visible = False
        
        if current_page == settings_page:
            settings_page.visible = True
            info_page.visible = False
            page.appbar.title = Text("Configuração")
        else:
            info_page.visible = True
            settings_page.visible = False
            page.appbar.title = Text("Sobre o App")
        sidebar.nav_rail.selected_index = None
        page.update()

    page.appbar = AppBar(
        title=Text("Página inicial"),
        center_title=True,
        color=Colors.WHITE,
        bgcolor=Colors.BLACK26,
        actions=[
            IconButton(
                Icons.INFO, on_click=lambda _: set_app_bar_pages(info_page)),
            IconButton(
                Icons.SETTINGS, on_click=lambda _: set_app_bar_pages(
                    settings_page)
            ),
        ],
    )

    sidebar = SideBar(
        page=page,
        main_page=main_page,
        decision=decision_page,
        rename=rename_page,
        memo=memo_page,
        other=others_page,
        info=info_page,
        settings=settings_page,
    )

    user_config = Path().joinpath(Path().home(), ".rsus/rsus_app_user.json")
    
    # Garantir que o diretório .rsus existe
    user_config.parent.mkdir(parents=True, exist_ok=True)

    def join_click(e):
        try:
            new_config = {}
            with open(user_config, "r", encoding="utf-8") as j:
                new_config = json.load(j)
                new_config["usuario"] = user_name.value

            with open(user_config, "w", encoding="utf-8") as j:
                json.dump(new_config, j, indent=2, ensure_ascii=False)

            name_dialog.open = False
            main_page.updater()
            page.update()
        except Exception as e:
            page.show_snack_bar(
                SnackBar(content=Text(f"Erro ao salvar configuração: {str(e)}"))
            )

    user_name = TextField(label="Digite seu nome de usuário")
    name_dialog = AlertDialog(
        modal=True,
        open=True,
        title=Text("Novo usuário"),
        content=Column([user_name], tight=True),
        actions=[ElevatedButton(text="Confirmar", on_click=join_click)],
    )

    # Carregar configuração do usuário
    try:
        if not user_config.exists():
            with open(user_config, "w", encoding="utf-8") as j:
                json.dump({"usuario": ""}, j, indent=2, ensure_ascii=False)
        
        with open(user_config, "r", encoding="utf-8") as j:
            config = json.load(j)

        if config.get("usuario", "") == "":
            page.overlay.append(name_dialog)
    except Exception as e:
        page.show_snack_bar(
            SnackBar(content=Text(f"Erro ao carregar configuração: {str(e)}"))
        )
        config = {"usuario": ""}
        page.overlay.append(name_dialog)

    # Criar a estrutura principal da aplicação
    app_win = Row(
        spacing=0,
        controls=[
            sidebar,
            Container(
                content=Row(
                    controls=all_pages,
                    alignment=MainAxisAlignment.CENTER,
                ),
                padding=padding.symmetric(vertical=25),
                # expand=True,
            ),
        ],
        expand=True,
    )

    # Adicionar a estrutura principal à página
    # page.horizontal_alignment = CrossAxisAlignment.CENTER
    page.add(app_win)

    # Atualizar a página inicialmente
    page.update()


if __name__ == "__main__":
    app(target=main)
