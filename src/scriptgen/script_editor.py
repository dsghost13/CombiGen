from PyQt6.Qsci import QsciScintilla
from PyQt6.QtCore import QFileSystemWatcher
from PyQt6.QtGui import QColor, QFont

from config.constants import SCRIPT_PATH


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

        self._internal_update = False

        self.load_file()
        self.watcher = QFileSystemWatcher([str(SCRIPT_PATH)])
        self.watcher.fileChanged.connect(self.file_changed)
        self.textChanged.connect(self.text_changed)

    def load_file(self):
        self._internal_update = True
        with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
            self.setText(f.read())
        self._internal_update = False

    def file_changed(self, path):
        if not self._internal_update:
            self.load_file()
        if path not in self.watcher.files():
            self.watcher.addPath(path)

    def text_changed(self):
        if not self._internal_update:
            with open(SCRIPT_PATH, "w", encoding="utf-8") as f:
                f.write(self.text())
