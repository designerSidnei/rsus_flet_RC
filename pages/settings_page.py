"""
Módulo que implementa a página de configurações do aplicativo RSUS.

Este módulo contém a implementação da página de configurações, que permite
ao usuário gerenciar dados de planilhas e configurações de usuário.
"""

import json
from flet import (
    AlertDialog,
    CrossAxisAlignment,
    Dropdown,
    ElevatedButton,
    ExpansionTile,
    MainAxisAlignment,
    Radio,
    RadioGroup,
    Row,
    Text,
    TextButton,
    TextField,
    Page,
    Column,
    Container,
    colors,
    dropdown,
)
from pathlib import Path


class Config(Column):
    """
    Página de configurações do aplicativo.

    Esta classe implementa a página de configurações que permite ao usuário:
    - Adicionar dados a planilhas (procedimentos, alegações, opiniões)
    - Gerenciar configurações de usuário
    - Resetar as configurações do usuário

    Args:
        page (Page): Página principal do aplicativo Flet
    """

    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.visible = False
        self.user_home_path = Path().joinpath(Path().home(), ".rsus/rsus_app_user.json")
        self.dlg = AlertDialog(
            modal=True,
            actions=[TextButton("OK", on_click=self.close_dlg)],
            actions_alignment=MainAxisAlignment.CENTER,
        )
        self.choose_plan_data = Dropdown(
            label="Dados da planilha",
            hint_text="Escolha qual o tipo de dado da planilha",
            on_change=self.show_options,
            options=[
                dropdown.Option("Nome do procedimento"),
                dropdown.Option("Alegação (Decisão)"),
                dropdown.Option("Opinião (Decisão)"),
            ],
            autofocus=True,
        )
        self.choose_group = RadioGroup(
            visible=False,
            content=Row(
                expand=True,
                alignment=MainAxisAlignment.SPACE_AROUND,
                controls=[
                    Radio(value="especial", label="Especial"),
                    Radio(value="consulta", label="Consulta"),
                    Radio(value="ambulatorial", label="Ambulatorial"),
                ],
            ),
        )

        self.campo_nome_procedimento = TextField()
        self.button_send = ElevatedButton("Incluir", on_click=self.submit)

        self.coluna_submit = Column(
            visible=False,
            spacing=10,
            horizontal_alignment=CrossAxisAlignment.CENTER,
            controls=[
                self.choose_group,
                self.campo_nome_procedimento,
                self.button_send,
            ],
        )

        self.list_coluna = [
            self.choose_plan_data,
            self.coluna_submit,
        ]

        self.expansion_panel_plan_data = ExpansionTile(
            title=Text("Acrescentar dados de planilha"),
            subtitle=Text("Selecione as opções"),
            controls=self.list_coluna,
            collapsed_bgcolor=colors.GREY_800,
            collapsed_text_color=colors.WHITE,
            controls_padding=20,
        )

        self.expansion_panel_user_config = ExpansionTile(
            title=Text("Configuração de usuário"),
            subtitle=Text("Resetar usuário"),
            controls=[TextButton("Resetar usuário", on_click=self.user_reset)],
            collapsed_bgcolor=colors.GREY_800,
            collapsed_text_color=colors.WHITE,
            controls_padding=20,
        )

        # Construir o conteúdo principal
        self.content = Container(
            expand=True,
            # width=660,
            width=self.page.window.width - 135,
            content=Column(
                controls=[
                    self.expansion_panel_plan_data,
                    self.expansion_panel_user_config,
                ],
                expand=True,
                alignment=MainAxisAlignment.START,
                spacing=5,
                scroll=True,
            ),
        )

        # Adicionar o conteúdo como controle do Column
        self.controls = [self.content]
        self.expand = True
        # self.alignment = MainAxisAlignment.CENTER

    def show_options(self, e):
        """
        Exibe as opções apropriadas com base na seleção do usuário no dropdown.

        Controla a visibilidade dos campos de entrada baseado no tipo de dado
        selecionado para a planilha.

        Args:
            e: Evento de mudança do dropdown
        """
        if self.choose_plan_data.value == "Nome do procedimento":
            self.choose_group.visible = True
            self.coluna_submit.visible = True
            self.campo_nome_procedimento.hint_text = "Nome do procedimento"
        elif self.choose_plan_data.value == "Alegação (Decisão)":
            self.choose_group.visible = False
            self.coluna_submit.visible = True
            self.campo_nome_procedimento.hint_text = "Alegação da decisão"
        elif self.choose_plan_data.value == "Opinião (Decisão)":
            self.choose_group.visible = False
            self.coluna_submit.visible = True
            self.campo_nome_procedimento.hint_text = "Opinião da decisão"
        else:
            self.coluna_submit.visible = False
        self.expansion_panel_plan_data.update()
        self.page.update()

    def submit(self, e):
        """
        Processa o envio de novos dados para a configuração.

        Adiciona o novo item à categoria apropriada no arquivo de configuração
        e exibe uma mensagem de confirmação.

        Args:
            e: Evento do botão de envio
        """
        config = {}
        msg = ""

        with open("./dados/config.json", "r", encoding="utf-8") as j:
            config = json.load(j)

        if self.campo_nome_procedimento.value != "":
            if self.choose_plan_data.value == "Nome do procedimento":
                try:
                    config["nome_procedimento"][self.choose_group.value].append(
                        self.campo_nome_procedimento.value
                    )
                    msg = f"{
                        self.campo_nome_procedimento.value} adicionado a 'Nome do procedimento'."
                except KeyError:
                    msg = "Nenhuma das opções marcadas. Selecione uma opção."
            elif self.choose_plan_data.value == "Alegação (Decisão)":
                config["lista_alegacao_decisao"].append(
                    self.campo_nome_procedimento.value
                )
                msg = f"{
                    self.campo_nome_procedimento.value} adicionado a 'Alegação'."
            elif self.choose_plan_data.value == "Opinião (Decisão)":
                config["lista_opiniao_decisao"].append(
                    self.campo_nome_procedimento.value
                )
                msg = f"{
                    self.campo_nome_procedimento.value} adicionado a 'Opinião'."
            with open("./dados/config.json", "w", encoding="utf-8") as j:
                json.dump(config, j, indent=2, ensure_ascii=False)

            self.campo_nome_procedimento.value = ""
            self.expansion_panel_plan_data.update()
        else:
            msg = "Campo vazio! Digite um valor."

        self.dlg.title = Text("Concluído")
        self.dlg.content = Text(msg)
        self.page.dialog = self.dlg
        self.dlg.open = True
        self.page.update()

    def user_reset(self, e):
        """
        Reseta as configurações do usuário.

        Remove o nome do usuário atual das configurações e exibe uma mensagem
        solicitando que o programa seja reiniciado.

        Args:
            e: Evento do botão de reset
        """
        config = {}

        with open(self.user_home_path, "r", encoding="utf-8") as j:
            config = json.load(j)
        config["usuario"] = ""

        with open(self.user_home_path, "w", encoding="utf-8") as j:
            json.dump(config, j, indent=2, ensure_ascii=False)

        self.dlg.title = Text("Concluído")
        self.dlg.content = Text(
            "Usuário resetado. Reinicie o programa para configurar um novo usuário.")
        self.page.dialog = self.dlg
        self.dlg.open = True
        self.page.update()

    def close_dlg(self, e):
        """
        Fecha o diálogo de mensagem.

        Args:
            e: Evento do botão de fechar
        """
        self.dlg.open = False
        self.page.update()
