from PyQt6.Qsci import QsciScintilla
from PyQt6.QtCore import QFileSystemWatcher, Qt
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget

from config.constants import F, SCAN_PATH, SCRIPT_PATH
from config.stylesheet import gen_button_ss, section_ss
from scriptgen import script_scan


class ScriptGen(QWidget):
    def __init__(self, combi_gen):
        super().__init__()

        section_layout = QVBoxLayout()
        section_layout.addWidget(LoadButton(combi_gen), alignment=Qt.AlignmentFlag.AlignCenter)

        section_widget = QWidget()
        section_widget.setStyleSheet(section_ss)
        section_widget.setLayout(section_layout)

        scriptgen_layout = QVBoxLayout()
        scriptgen_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        scriptgen_layout.setContentsMargins(0, 0, 0, 0)
        scriptgen_layout.setSpacing(0)

        scriptgen_layout.addWidget(ScriptEditor())
        scriptgen_layout.addWidget(section_widget)
        self.setLayout(scriptgen_layout)


class ScriptEditor(QsciScintilla):
    def __init__(self):
        super().__init__()

        font = QFont("Consolas", 9)
        self.setFont(font)
        self.setMarginsFont(font)

        line_number_fg = QColor("#606366")
        line_number_bg = QColor("#313335")
        self.setMarginType(0, QsciScintilla.MarginType.NumberMargin)
        self.setMarginWidth(0, "000")
        self.setMarginsForegroundColor(line_number_fg)
        self.setMarginsBackgroundColor(line_number_bg)

        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor("#323232"))
        self.setCaretForegroundColor(QColor("#FFFFFF"))

        self.setIndentationsUseTabs(False)
        self.setTabWidth(4)
        self.setAutoIndent(True)

        self.setUtf8(True)
        self.setBraceMatching(QsciScintilla.BraceMatch.SloppyBraceMatch)
        self.setMatchedBraceBackgroundColor(QColor("#888888"))
        self.setMatchedBraceForegroundColor(QColor("#FFFFFF"))

        self.internal_update = False
        self.setEolMode(QsciScintilla.EolMode.EolUnix)

        self.load_file()
        self.watcher = QFileSystemWatcher([str(SCRIPT_PATH)])
        self.watcher.fileChanged.connect(self.file_changed)
        self.textChanged.connect(self.text_changed)

    def load_file(self):
        self.internal_update = True
        line, index = self.getCursorPosition()
        with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
            self.setText(f.read())
        self.setCursorPosition(line, index)
        self.internal_update = False

    def file_changed(self, path):
        if not self.internal_update:
            self.load_file()
        if path not in self.watcher.files():
            self.watcher.addPath(path)

    def text_changed(self):
        if not self.internal_update:
            with open(SCRIPT_PATH, "w", encoding="utf-8") as f:
                f.write(self.text())


class LoadButton(QPushButton):
    def __init__(self, combi_gen):
        super().__init__()
        self.combi_gen = combi_gen
        self.setFixedHeight(39)
        self.setFixedWidth(110)
        self.setSizePolicy(F, F)
        self.setStyleSheet(gen_button_ss)
        self.setText(" Load Configs ")
        self.pressed.connect(self.load_configs)

    def load_configs(self):
        try:
            lines = SCRIPT_PATH.read_text(encoding="utf-8").splitlines()
            if len(lines) < 22:
                raise Exception("LoadError: script is empty or does not follow standard format.")

            with open(SCRIPT_PATH, 'r', encoding="utf-8") as f:
                lines = f.readlines()
                num_lines = len(lines) - 9
                lines = lines[:num_lines]

            with open(SCAN_PATH, 'w', encoding="utf-8") as f:
                f.writelines(lines)

            for name, field_value in vars(script_scan).items():
                match name:
                    case "source_cores":
                        text = ', '.join(field_value)
                        self.combi_gen.source_widget.core_widget.core_text_entry.line_edit.setText(text)
                    case "source_subs":
                        subs = self.combi_gen.source_widget.sub_widget
                        while subs.subs_layout.count():
                            subs.subs_layout.takeAt(0).widget().deleteLater()
                        for i in range(len(field_value)):
                            text = ', '.join(field_value[i])
                            subs.add_substituent()
                            subs.subs_layout.itemAt(i).widget().layout().itemAt(1).widget().setText(text)
                    case "sink_cores":
                        text = ', '.join(field_value)
                        self.combi_gen.sink_widget.core_widget.core_text_entry.line_edit.setText(text)
                    case "sink_subs":
                        subs = self.combi_gen.sink_widget.sub_widget
                        while subs.subs_layout.count():
                            subs.subs_layout.takeAt(0).widget().deleteLater()
                        for i in range(len(field_value)):
                            text = ', '.join(field_value[i])
                            subs.add_substituent()
                            subs.subs_layout.itemAt(i).widget().layout().itemAt(1).widget().setText(text)
                    case "linkers":
                        text = ', '.join(field_value)
                        self.combi_gen.linker_widget.linker_text_entry.line_edit.setText(text)
                    case "arrow_pushing":
                        self.combi_gen.arrow_pushing_widget.arrow_pushing_text_entry.line_edit.setText(field_value)
                    case "pareto_fronts":
                        pfs = self.combi_gen.pareto_widget
                        while pfs.paretos_layout.count():
                            pfs.paretos_layout.takeAt(0).widget().deleteLater()
                        for i in range(len(field_value)):
                            pfs.add_pareto_front()
                            table = pfs.paretos_layout.itemAt(i).widget().layout().itemAt(2).widget().layout().itemAt(1).widget()

                            row_subs = ", ".join(field_value[i].index.astype(str))
                            col_subs = ", ".join(field_value[i].columns.astype(str))
                            table.row_select.update_dropdown()
                            table.col_select.update_dropdown()
                            row_idx = table.row_select.findText(row_subs)
                            col_idx = table.col_select.findText(col_subs)
                            if (row_idx != -1) and (col_idx != -1):
                                table.row_select.setCurrentIndex(row_idx)
                                table.col_select.setCurrentIndex(col_idx)
                            table.update_table()

                            for r, row_label in enumerate(field_value[i].index):
                                for c, col_label in enumerate(field_value[i].columns):
                                    truth_value = bool(field_value[i].at[row_label, col_label])
                                    cell_button = table.table_layout.itemAtPosition(r+1, c+1).widget()
                                    cell_button.setChecked(truth_value)
                    case _:
                        pass
        except Exception as e:
            print(e)