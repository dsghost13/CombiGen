from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QPushButton, QScrollArea, QVBoxLayout, QWidget, QMessageBox

from combigen.generic_widgets import TextEntryWidget
from combigen.pareto import ParetoWidget
from combigen.reactant import ReactantWidget
from config.constants import F, P
from config.stylesheet import gen_button_ss, scroll_area_ss, section_ss
from scriptgen.data_fields import TextEntryHandler
from scriptgen.script_gen import ScriptGenerator


class CombiGen(QScrollArea):
    def __init__(self):
        super().__init__()

        combigen_layout = QVBoxLayout()
        combigen_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        combigen_layout.setContentsMargins(0, 0, 0, 0)
        combigen_layout.setSpacing(0)

        self.source_widget = ReactantWidget("SOURCE")
        self.sink_widget = ReactantWidget("SINK")
        self.linker_widget = LinkerWidget()
        self.arrow_pushing_widget = ArrowPushingWidget()
        self.pareto_widget = ParetoWidget()

        combigen_layout.addWidget(self.source_widget)
        combigen_layout.addWidget(self.sink_widget)
        combigen_layout.addWidget(self.linker_widget)
        combigen_layout.addWidget(self.arrow_pushing_widget)
        combigen_layout.addWidget(self.pareto_widget)
        combigen_layout.addWidget(GenerateButton())

        combigen_widget = QWidget()
        combigen_widget.setLayout(combigen_layout)

        self.setStyleSheet(scroll_area_ss)
        self.setWidget(combigen_widget)
        self.setWidgetResizable(True)


class LinkerWidget(QWidget):
    def __init__(self):
        super().__init__()

        linker_label = QLabel("LINKER")
        linker_label.setSizePolicy(P, F)

        self.linker_text_entry = TextEntryWidget("Linker(s)", "linkers")

        linker_layout = QVBoxLayout()
        linker_layout.addWidget(linker_label)
        linker_layout.addWidget(self.linker_text_entry)

        linker_widget = QWidget()
        linker_widget.setLayout(linker_layout)
        linker_widget.setStyleSheet(section_ss)

        wrapper_layout = QVBoxLayout()
        wrapper_layout.addWidget(linker_widget)
        self.setLayout(wrapper_layout)


class ArrowPushingWidget(QWidget):
    def __init__(self):
        super().__init__()

        arrow_pushing_label = QLabel("ARROW PUSHING")
        arrow_pushing_label.setSizePolicy(P, F)

        self.arrow_pushing_text_entry = TextEntryWidget("Arrow Pushing", "arrow_pushing")

        arrow_pushing_layout = QVBoxLayout()
        arrow_pushing_layout.addWidget(arrow_pushing_label)
        arrow_pushing_layout.addWidget(self.arrow_pushing_text_entry)

        arrow_pushing_widget = QWidget()
        arrow_pushing_widget.setLayout(arrow_pushing_layout)
        arrow_pushing_widget.setStyleSheet(section_ss)

        wrapper_layout = QVBoxLayout()
        wrapper_layout.addWidget(arrow_pushing_widget)
        self.setLayout(wrapper_layout)


class GenerateButton(QWidget):
    def __init__(self):
        super().__init__()

        gen_button = QPushButton(" Generate Script ")
        gen_button.setFixedHeight(40)
        gen_button.setSizePolicy(F, F)
        gen_button.setStyleSheet(gen_button_ss)
        gen_button.pressed.connect(self.generate_script)

        gen_button_layout = QVBoxLayout()
        gen_button_layout.addWidget(gen_button)
        gen_button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setLayout(gen_button_layout)
        self.setStyleSheet(section_ss)

    def generate_script(self):
        if not TextEntryHandler.DATA["source_cores"]:
            WarningMessageBox("Source core(s) not found!").exec()
            return
        if not TextEntryHandler.DATA["sink_cores"]:
            WarningMessageBox("Sink core(s) not found!").exec()
            return
        if not TextEntryHandler.DATA["arrow_pushing"]:
            WarningMessageBox("Arrow pushing not found!").exec()
            return

        try:
            ScriptGenerator.generate_script()
        except Exception as e:
            print(e)


class WarningMessageBox(QMessageBox):
    def __init__(self, text):
        super().__init__()
        self.setIcon(QMessageBox.Icon.Warning)
        self.setText(text)
        self.setWindowTitle("WARNING")