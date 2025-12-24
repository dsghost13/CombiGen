import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QMainWindow, QTabWidget, QVBoxLayout, QWidget

from src.config.constants import E
from src.combi_gen.main_ui import CombiGen
from src.output_gen.output import OutputGenerator
from src.script_gen.script_editor import ScriptEditor


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        main_layout = QHBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_layout.addWidget(get_tab_widget())

        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        self.setWindowTitle("CombiGen")
        self.showMaximized()


def get_tab_widget():
    tabs = QTabWidget()
    tabs.setLayout(QVBoxLayout())
    tabs.setMovable(True)
    tabs.setSizePolicy(E, E)
    tabs.setTabPosition(QTabWidget.TabPosition.North)

    tabs.addTab(CombiGen(), "CombiGen")
    tabs.addTab(ScriptEditor(), "Script Editor")
    tabs.addTab(OutputGenerator(), "Output SMILES")
    return tabs


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()


if __name__  == "__main__":
    main()