import csv
import random
import subprocess

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QTextCursor
from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget, QTextEdit

from combigen.generic_widgets import TextEntryWidget
from config.constants import F, TXT_PATH, SCRIPT_PATH, CSV_PATH
from config.stylesheet import gen_button_ss, section_ss, terminal_ss
from scriptgen.data_fields import TextEntryHandler


class OutputGen(QWidget):
    def __init__(self):
        super().__init__()

        output_text_entry = TextEntryWidget("Output Proportion", "output_proportion")
        output_text_entry.line_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        output_text_entry.line_edit.setFixedWidth(50)
        output_text_entry.line_edit.setText(str(TextEntryHandler.DATA["output_proportion"]))

        run_button = RunButton()
        output_terminal = OutputTerminal()

        section_layout = QVBoxLayout()
        section_layout.addWidget(output_text_entry, alignment=Qt.AlignmentFlag.AlignLeft)
        section_layout.addWidget(run_button, alignment=Qt.AlignmentFlag.AlignCenter)

        section_widget = QWidget()
        section_widget.setStyleSheet(section_ss)
        section_widget.setLayout(section_layout)

        output_layout = QVBoxLayout()
        output_layout.addWidget(section_widget)
        output_layout.addWidget(output_terminal)
        output_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        output_layout.setContentsMargins(9, 9, 9, 9)
        output_layout.setSpacing(0)
        self.setLayout(output_layout)


class RunButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(39)
        self.setFixedWidth(110)
        self.setSizePolicy(F, F)
        self.setStyleSheet(gen_button_ss)
        self.setText(" Run Script ")
        self.pressed.connect(self.run_script)

    def run_script(self):
        try:
            lines = SCRIPT_PATH.read_text(encoding="utf-8").splitlines()
            if len(lines) < 22:
                return

            lines[-3] = f"\tif random.random() <= 1:"
            SCRIPT_PATH.write_text("\n".join(lines), encoding="utf-8")
            output = subprocess.run(["python", SCRIPT_PATH], capture_output=True, text=True)
            output_lines = output.stdout.splitlines()

            with open(CSV_PATH, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["SMILES Labelled"])
                for line in output_lines[:-1]:
                    writer.writerow([line])

            output_proportion = TextEntryHandler.DATA["output_proportion"]
            selected = [line for line in output_lines if random.random() < output_proportion]
            with open(TXT_PATH, "w", encoding="utf-8") as f:
                f.writelines(f"{line}\n" for line in selected)
                f.write(output_lines[-1])
                f.write(output.stderr)

            lines[-3] = f"\tif random.random() < {output_proportion}:"
            SCRIPT_PATH.write_text("\n".join(lines), encoding="utf-8")
        except Exception as e:
            print(e)

class OutputTerminal(QWidget):
    def __init__(self):
        super().__init__()
        self.last_text = TXT_PATH.read_text(encoding="utf-8", errors="ignore")

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setStyleSheet(terminal_ss)
        self.text_edit.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        self.text_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        terminal_layout = QVBoxLayout(self)
        terminal_layout.addWidget(self.text_edit)
        self.setLayout(terminal_layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.display_output)
        self.timer.start(500)

    def display_output(self):
        text = TXT_PATH.read_text(encoding="utf-8", errors="ignore")
        if text != self.last_text:
            self.last_text = text
            self.text_edit.setPlainText(text)
            self.text_edit.moveCursor(QTextCursor.MoveOperation.End)