from PyQt6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QPushButton, QWidget

from config.constants import F
from scriptgen.data_fields import TextEntryHandler
from config.stylesheet import add_button_ss, del_button_ss, text_entry_ss


class TextEntryWidget(QWidget):
    def __init__(self, caption, field):
        super().__init__()
        self.field = field

        caption_label = QLabel(f"{caption}: ")

        self.line_edit = QLineEdit()
        self.line_edit.setStyleSheet(text_entry_ss)
        self.line_edit.textChanged.connect(self.update_field)

        text_entry_layout = QHBoxLayout()
        text_entry_layout.addWidget(caption_label)
        text_entry_layout.addWidget(self.line_edit)

        self.setLayout(text_entry_layout)

    def update_field(self):
        text = self.line_edit.text()
        if text != "":
            TextEntryHandler.update_field(self.field, text)


class AddButton(QPushButton):
    def __init__(self, name):
        super().__init__()
        self.setText(f" + Add {name}  ")
        self.setFixedHeight(20)
        self.setSizePolicy(F, F)
        self.setStyleSheet(add_button_ss)


class DeleteButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.setText("   -   ")
        self.setFixedHeight(20)
        self.setSizePolicy(F, F)
        self.setStyleSheet(del_button_ss)