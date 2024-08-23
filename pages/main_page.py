from flet import Column, Page, Row, Text

# from datetime import datetime
# import time

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
        # self.date_now = Text(size=20,)
        # self.today_datetime()

    def build(self):
        return Column(
            [
                self.user_text,
                # self.date_now,
            ],
        )

    # def today_datetime(self):
    #    self.date_now.value = str(datetime.now())
    #    time.sleep(1)
    #    self.page.update()

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

