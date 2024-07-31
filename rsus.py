from flet import (
    Page,
    app,
    AppBar,
    NavigationRailDestination,
    NavigationRailLabelType,
    NavigationRail,
    Text,
    Container,
    Column,
    Row,
    MainAxisAlignment,
    CrossAxisAlignment,
    IconButton,
    margin,
    padding,
    icons,
    colors,
)

from pages.main_page import MainPage
from pages.decision_page import Decisao
from pages.rename_page import Rename
from pages.memo_page import Memo
from pages.others_page import Outros
from pages.settings_page import Config
from pages.info_page import Info


class SideBar(Row):
    def __init__(
        self,
        page: Page,
        main_page: Row,
        dicision: Row,
        rename: Row,
        memo: Column,
        other: Row,
        info: Column,
        settings: Column,
    ):
        super().__init__()
        self.page = page
        self.main_page = main_page
        self.dicision = dicision
        self.rename = rename
        self.memo = memo
        self.other = other
        self.settings = settings
        self.info = info

        self.nav_itens = [
            NavigationRailDestination(
                label_content=Text("Página inicial"),
                label="Página inicial",
                icon=icons.HOME,
                selected_icon=icons.HOME_OUTLINED,
            ),
            NavigationRailDestination(
                label_content=Text("Decisão"),
                label="Decisão",
                icon=icons.ACCESS_TIME_FILLED,
                selected_icon=icons.ACCESS_TIME_OUTLINED,
            ),
            NavigationRailDestination(
                label_content=Text("Renomear"),
                label="Renomear",
                icon=icons.EDIT,
                selected_icon=icons.EDIT_OUTLINED,
            ),
            NavigationRailDestination(
                label_content=Text("Memória"),
                label="Memória",
                icon=icons.NUMBERS,
                selected_icon=icons.NUMBERS_OUTLINED,
            ),
            NavigationRailDestination(
                label_content=Text("Outros"),
                label="Outros",
                icon=icons.MORE,
                selected_icon=icons.MORE_OUTLINED,
            ),
        ]

        self.nav_rail = NavigationRail(
            selected_index=0,
            expand=True,
            label_type=NavigationRailLabelType.ALL,
            on_change=self.mudar_pagina,
            destinations=self.nav_itens,
            bgcolor=colors.BLACK12,
            height=310,
        )

    def build(self):
        self.view = Container(
            content=Column(
                controls=[
                    self.nav_rail,
                ],
                # tight=True,
                expand=True,
            ),
            padding=0,
            margin=margin.all(0),
            width=120,
        )
        return self.view

    def mudar_pagina(self, e):
        index = e if (type(e) == int) else e.control.selected_index
        self.view.update()
        if index == 0:
            self.page.appbar.title = Text("Página inicial")
            self.main_page.visible = True
            self.dicision.visible = False
            self.rename.visible = False
            self.memo.visible = False
            self.other.visible = False
            self.settings.visible = False
            self.info.visible = False
        elif index == 1:
            self.page.appbar.title = Text("Decisão")
            self.main_page.visible = False
            self.dicision.visible = True
            self.rename.visible = False
            self.memo.visible = False
            self.other.visible = False
            self.settings.visible = False
            self.info.visible = False
        elif index == 2:
            self.page.appbar.title = Text("Renomear")
            self.main_page.visible = False
            self.dicision.visible = False
            self.rename.visible = True
            self.memo.visible = False
            self.other.visible = False
            self.settings.visible = False
            self.info.visible = False
        elif index == 3:
            self.page.appbar.title = Text("Memória de cálculo")
            self.main_page.visible = False
            self.dicision.visible = False
            self.rename.visible = False
            self.memo.visible = True
            self.other.visible = False
            self.settings.visible = False
            self.info.visible = False
        elif index == 4:
            self.page.appbar.title = Text("Outras opções")
            self.main_page.visible = False
            self.dicision.visible = False
            self.rename.visible = False
            self.memo.visible = False
            self.other.visible = True
            self.settings.visible = False
            self.info.visible = False
        self.page.update()


def main(page: Page):
    page.title = "RSUS"
    page.window.width = 800
    page.window.height = 520
    page.window.maximizable = False
    page.window.resizable = False
    page.window.center()
    page.padding = 0

    main_page = MainPage()
    decision_page = Decisao(page)
    rename_page = Rename(page)
    memo_page = Memo(page)
    others_page = Outros(page)
    info_page = Info(page)
    settings_page = Config(page)

    page.appbar = AppBar(
        title=Text("Página inicial"),
        center_title=True,
        bgcolor=colors.BLACK26,
        actions=[
            IconButton(icons.INFO, on_click=lambda _: set_app_bar_pages(info_page)),
            IconButton(
                icons.SETTINGS, on_click=lambda _: set_app_bar_pages(settings_page)
            ),
        ],
    )

    sidebar = SideBar(
        page=page,
        main_page=main_page,
        dicision=decision_page,
        rename=rename_page,
        memo=memo_page,
        other=others_page,
        info=info_page,
        settings=settings_page,
    )

    def set_app_bar_pages(current_page: Row):
        if current_page == settings_page:
            settings_page.visible = True
            info_page.visible = False
            page.appbar.title = Text("Configuração")
        else:
            info_page.visible = True
            settings_page.visible = False
            page.appbar.title = Text("Sobre o App")
        sidebar.nav_rail.selected_index = None
        main_page.visible = False
        decision_page.visible = False
        rename_page.visible = False
        memo_page.visible = False
        others_page.visible = False
        page.update()
        sidebar.view.update()

    app_win = Row(
        spacing=0,
        controls=[
            sidebar,
            Container(
                content=Row(
                    [
                        main_page,
                        decision_page,
                        rename_page,
                        memo_page,
                        others_page,
                        info_page,
                        settings_page,
                    ],
                    alignment=MainAxisAlignment.CENTER,
                ),
                padding=padding.symmetric(vertical=25),
                expand=True,
            ),
        ],
        expand=True,
    )
    page.horizontal_alignment = CrossAxisAlignment.CENTER
    page.add(app_win)
    page.update()


if __name__ == "__main__":
    app(target=main)
