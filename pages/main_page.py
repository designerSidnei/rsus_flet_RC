"""
Módulo que implementa a página inicial do aplicativo RSUS.

Este módulo contém a implementação da página inicial, que exibe
informações básicas como nome do usuário e hora atual.
"""

from flet import Column, Page, Row, Text, CrossAxisAlignment, Container

from datetime import datetime
from pathlib import Path

import os
import json
import asyncio


class MainPage(Row):
    """
    Página inicial do aplicativo.

    Esta classe implementa a página inicial que exibe uma saudação ao usuário
    e um relógio digital atualizado em tempo real.

    Args:
        page (Page): Página principal do aplicativo Flet
    """

    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.user = self.congig_user()
        self.user_text = Text(
            value=self.user,
            size=35,
        )

        self.past = datetime.now()
        self.date_now = Text(
            value=datetime.now().strftime("%d/%m/%Y"), size=20,)
        self.time_now = Text(size=20,)
        self.date_time_now = Container(
            content=Column(
                expand=True,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                spacing=0,
                controls=[
                    self.date_now, self.time_now],
            ),
        )

        # Construir o conteúdo principal
        self.content = Column(
            horizontal_alignment=CrossAxisAlignment.CENTER,
            controls=[
                self.user_text,
                self.date_time_now,
            ],
            width=self.page.window.width - 135,
        )

        # Adicionar o conteúdo como controle do Row
        self.controls = [self.content]
        self.expand = True
        # self.alignment = MainAxisAlignment.END

    def did_mount(self):
        """
        Método chamado quando o componente é montado.
        
        Inicia a tarefa assíncrona de atualização do relógio.
        """
        self.running = True
        self.page.run_task(self.today_datetime)

    async def today_datetime(self):
        """
        Atualiza o relógio digital a cada segundo.

        Este método é executado de forma assíncrona para manter
        o relógio atualizado sem bloquear a interface.
        """
        while self.running:
            if datetime.now() > self.past:
                self.time_now.value = datetime.now().strftime("%H:%M:%S")
            else:
                self.time_now.value = str(self.past)
            self.page.update()
            try:
                await asyncio.sleep(1)
            except asyncio.exceptions.CancelledError:
                break
            except Exception:
                print("")

    def congig_user(self):
        """
        Carrega e retorna a mensagem de boas-vindas personalizada para o usuário.

        Returns:
            str: Mensagem de boas-vindas com o nome do usuário ou mensagem genérica
                caso não haja usuário configurado.
        """
        user_config = {}
        user_home_path = Path().joinpath(Path().home(), ".rsus")
        os.makedirs(user_home_path, exist_ok=True)
        user_new_path = Path().joinpath(user_home_path, "rsus_app_user.json")
        if not user_new_path.exists():
            with open(user_new_path, "w", encoding="utf-8") as j:
                json.dump({"usuario": ""}, j, indent=2, ensure_ascii=False)

        user = ""
        with open(user_new_path, "r", encoding="utf-8") as j:
            user_config = json.load(j)
            user = user_config["usuario"]

        if user == "":
            return "Olá, Usuário!\nBem vindo!"
        else:
            return f"Olá, {user}!\nBem vindo!"

    def updater(self):
        """
        Atualiza a mensagem de boas-vindas na interface.
        
        Este método é chamado quando há alterações nas configurações do usuário.
        """
        self.user = self.congig_user()
        self.user_text.value = self.user
        self.page.update()
