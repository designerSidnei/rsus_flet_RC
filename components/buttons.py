from flet import (Page, Row, icons, TextField, FilePicker, FilePickerFileType, FilePickerResultEvent, ElevatedButton
)


class Buttons(Row):
    def __init__(self, page: Page, button_text: str, button_icon: icons, path_text_field: TextField, file_type: list):
        super().__init__()
        self.page = page
        self.file_picker = FilePicker(on_result=self.pick_files_result)
        self.button_text = button_text
        self.button_icon = button_icon
        self.path_text_field = path_text_field
        self.file_type = file_type

        # Atributo para armazenar o TextField alvo atual
        self.current_target_field = None
        self._path_name = ""

        """ def build(self):
            self.page.overlay.append(self.file_picker)
            return ElevatedButton(
                text=self.button_text,
                height=50,
                width=140,
                icon=self.button_icon,
                on_click=lambda _: self.set_target_and_pick_files(self.path_text_field, self.file_type)
            ) """
    
        self.content = ElevatedButton(
            text=self.button_text,
            height=50,
            width=140,
            icon=self.button_icon,
            on_click=lambda _: self.set_target_and_pick_files(self.path_text_field, self.file_type)
        )
        
        self.page.overlay.append(self.file_picker)
        self.controls = [self.content]
        

    def set_target_and_pick_files(self, target_field: TextField, file_type):
        # Define o TextField alvo e inicia a seleção de arquivos
        self.current_target_field = target_field
        self.file_picker.pick_files(allow_multiple=True, file_type=FilePickerFileType.CUSTOM,
                                    allowed_extensions=file_type)

    def pick_files_result(self, e: FilePickerResultEvent):
        # Atualiza o TextField alvo com os nomes dos arquivos selecionados
        if self.current_target_field:
            self.current_target_field.set_text((", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelado!"))
            self._path_name = (", ".join(map(lambda f: f.path, e.files)) if e.files else "")
            # self.on_change_path_name()
            self.current_target_field.update()

    @property
    def path_name(self):
        return self._path_name

    def on_change_path_name(self):
        if self.path_name != "":
            print(self.path_name)


class DirButton(Row):
    def __init__(self, button_text: str, button_icon: icons, path_text_field: TextField):
        super().__init__()
        self.folder_picker = FilePicker(on_result=self.pick_files_result)
        self.button_text = button_text
        self.button_icon = button_icon
        self.path_text_field = path_text_field

        # Atributo para armazenar o TextField alvo atual
        self.current_target_field = None
        self._path_name = ""

    def build(self):
        self.page.overlay.append(self.folder_picker)
        return ElevatedButton(
            text=self.button_text,
            height=50,
            width=140,
            icon=self.button_icon,
            on_click=lambda _: self.set_target_and_pick_files(self.path_text_field)
        )

    def set_target_and_pick_files(self, target_field: TextField):
        # Define o TextField alvo e inicia a seleção de arquivos
        self.current_target_field = target_field
        self.folder_picker.get_directory_path()

    def pick_files_result(self, e: FilePickerResultEvent):
        # Atualiza o TextField alvo com os nomes dos arquivos selecionados
        if self.current_target_field:
            self.current_target_field.set_text(e.path if e.path else "Cancelado!")
            self._path_name = (e.path if e.path else "Cancelado!")
            self.current_target_field.update()
    
    @property
    def path_name(self):
        return self._path_name
