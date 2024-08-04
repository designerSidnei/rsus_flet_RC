from flet import Column, Row, Text


class MainPage(Row):
    def build(self):
        self.win_title = Column(
            [
                Text(
                    value="Olá, Sidnei!\nBem vindo!",
                    size=25,
                ),
            ],
        )
        return self.win_title
