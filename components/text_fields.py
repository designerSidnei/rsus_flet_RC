from flet import TextField, UserControl

class CustomTextField(UserControl):
    def __init__(self, hint: str):
        super().__init__()
        self.hint = hint
        self.text_field = TextField(hint_text=self.hint, width=350, read_only=True)
        self._text_field_value = self.text_field.value
    def build(self):
        return self.text_field
    
    def set_text(self, text):
        self.text_field.value = text

    @property
    def text_field_value(self):
        return self._text_field_value
        