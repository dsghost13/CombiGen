from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt6.QtWidgets import QLabel, QLineEdit, QWidget

from combigen.generic_widgets import DeleteButton, AddButton, TextEntryWidget
from config.constants import F, P
from scriptgen.data_fields import TextEntryHandler
from config.stylesheet import section_ss, text_entry_ss


class ReactantWidget(QWidget):
    def __init__(self, reactant_type):
        super().__init__()

        reactant_label = QLabel(reactant_type)
        reactant_label.setSizePolicy(P, F)

        core_widget = CoreWidget(reactant_type)
        sub_widget = SubstituentWidget(reactant_type)

        reactant_layout = QVBoxLayout()
        reactant_layout.setSpacing(0)
        reactant_layout.addWidget(reactant_label)
        reactant_layout.addWidget(core_widget)
        reactant_layout.addWidget(sub_widget)

        reactant_widget = QWidget()
        reactant_widget.setLayout(reactant_layout)
        reactant_widget.setSizePolicy(P, F)
        reactant_widget.setStyleSheet(section_ss)

        # bypass style sheet issues when inheriting from QWidget
        wrapper_layout = QVBoxLayout()
        wrapper_layout.addWidget(reactant_widget)
        self.setLayout(wrapper_layout)


class CoreWidget(QWidget):
    def __init__(self, reactant_type):
        super().__init__()
        self.reactant_type = reactant_type

        core_text_entry = TextEntryWidget("Core(s)", f"{self.reactant_type.lower()}_cores")

        core_layout = QVBoxLayout()
        core_layout.addWidget(core_text_entry)
        self.setLayout(core_layout)


class SubstituentWidget(QWidget):
    def __init__(self, reactant_type):
        super().__init__()
        self.reactant_type = reactant_type

        sub_label = QLabel("Substituent(s): ")

        add_button = AddButton("Substituent")
        add_button.clicked.connect(self.add_substituent)

        # substituents
        self.subs_layout = QVBoxLayout()
        self.subs_layout.setContentsMargins(0, 0, 0, 0)
        self.subs_layout.setSpacing(0)

        subs_widget = QWidget()
        subs_widget.setLayout(self.subs_layout)

        # label + substituents + button
        module_layout = QVBoxLayout()
        module_layout.addWidget(sub_label)
        module_layout.addWidget(subs_widget)
        module_layout.addWidget(add_button)
        self.setLayout(module_layout)

    def add_substituent(self):
        del_button = DeleteButton()

        sub_text_entry = QLineEdit()
        sub_text_entry.setStyleSheet(text_entry_ss)

        sub_layout = QHBoxLayout()
        sub_layout.setContentsMargins(5, 5, 0, 0)
        sub_layout.addWidget(del_button)
        sub_layout.addWidget(sub_text_entry)

        sub_widget = QWidget()
        sub_widget.setLayout(sub_layout)
        self.subs_layout.addWidget(sub_widget)

        sub_text_entry.textChanged.connect(self.update_field)
        del_button.clicked.connect(lambda: self.delete_substituent(sub_widget))

    def delete_substituent(self, sub_widget: QWidget):
        self.subs_layout.removeWidget(sub_widget)
        self.update_field()

    def update_field(self):
        text = []
        for i in range(self.subs_layout.count()):
            sub_layout = self.subs_layout.itemAt(i).widget().layout()
            sub_text = sub_layout.itemAt(1).widget().text()
            text.append(sub_text)

        field = f"{self.reactant_type.lower()}_subs"
        TextEntryHandler.update_field(field, text)