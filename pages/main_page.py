from flet import Column, Page, Row, Text, CrossAxisAlignment

from datetime import datetime
import asyncio

from modules.load_config import config_read


class MainPage(Row):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.config = config_read()
        self.user = self.congig_user()
        self.user_text = Text(
            value=self.user,
            size=25,
        )

        self.past = datetime.now()
        self.date_now = Text(value=datetime.now().strftime("%d/%m/%Y"), size=20,)
        self.time_now = Text(size=20,)

    def did_mount(self):
        self.running = True
        self.page.run_task(self.today_datetime)

    # def will_unmount(self):
    #     self.running = False

    def build(self):
        return Column(
            horizontal_alignment=CrossAxisAlignment.CENTER,
            controls=[
                self.user_text,
                self.date_now,
                self.time_now,
            ],
        )

    async def today_datetime(self):
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
        user = self.config["usuario"]
        if user == "":
            return "Olá, Usuário!\nBem vindo!"
        else:
            return f"Olá, {user}!\nBem vindo!"

    def updater(self):
        self.config = config_read()
        self.user = self.congig_user()
        self.user_text.value = self.user
        self.page.update()
