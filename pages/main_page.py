from flet import Column, Row, Text, Page
from modules.load_config import config_read



class MainPage(Row):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.config = config_read()

    def build(self):
        self.win_title = Column(
            [
                Text(
                    value=f"Olá, {self.config["usuario"]}!\nBem vindo!",
                    size=25,
                ),
            ],
            
        )
        # self.page.update() 
        return self.win_title
