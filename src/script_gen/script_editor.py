from PyQt6.Qsci import QsciScintilla, QsciLexerPython
from PyQt6.QtGui import QFont, QColor
from matplotlib.backend_tools import cursors


class ScriptEditor(QsciScintilla):
    def __init__(self):
        super().__init__()

        # font
        font = QFont("Consolas", 9)
        self.setFont(font)
        self.setMarginsFont(font)

        # theme colors
        bg_color = QColor("#1E1F22")
        fg_color = QColor("#AABDC3")
        cursor_color = QColor("#A9B7C6")
        current_line = QColor("#323232")
        line_number_fg = QColor("#606366")
        line_number_bg = QColor("#313335")

        # editor colors
        self.setPaper(bg_color)
        self.setColor(fg_color)
        self.setCaretForegroundColor(cursor_color)
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(current_line)

        # selection
        self.setSelectionBackgroundColor(QColor("#214283"))
        self.setSelectionForegroundColor(QColor("#FFFFFF"))

        # line numbers
        self.setMarginType(0, QsciScintilla.MarginType.NumberMargin)
        # Make margin wide enough for 9999 lines (monospaced)
        self.setMarginWidth(0, "0000")
        self.setMarginsForegroundColor(line_number_fg)
        self.setMarginsBackgroundColor(line_number_bg)

        # indentation
        self.setIndentationsUseTabs(False)
        self.setTabWidth(4)
        self.setAutoIndent(True)
        self.setIndentationGuides(True)

        # brace matching
        self.setBraceMatching(QsciScintilla.BraceMatch.SloppyBraceMatch)
        self.setMatchedBraceBackgroundColor(QColor("#3B514D"))
        self.setMatchedBraceForegroundColor(QColor("#FFFFFF"))

        # Python lexer
        lexer = QsciLexerPython(self)
        lexer.setDefaultFont(font)
        lexer.setDefaultPaper(bg_color)
        lexer.setDefaultColor(fg_color)

        # PyCharm syntax colors
        lexer.setColor(QColor("#CC7832"), QsciLexerPython.Keyword)
        lexer.setColor(QColor("#A9B7C6"), QsciLexerPython.Default)
        lexer.setColor(QColor("#6A8759"), QsciLexerPython.Comment)
        lexer.setColor(QColor("#6A8759"), QsciLexerPython.CommentBlock)
        lexer.setColor(QColor("#9876AA"), QsciLexerPython.Number)
        lexer.setColor(QColor("#6897BB"), QsciLexerPython.SingleQuotedString)
        lexer.setColor(QColor("#6897BB"), QsciLexerPython.DoubleQuotedString)
        lexer.setColor(QColor("#6897BB"), QsciLexerPython.TripleSingleQuotedString)
        lexer.setColor(QColor("#6897BB"), QsciLexerPython.TripleDoubleQuotedString)
        lexer.setColor(QColor("#FFC66D"), QsciLexerPython.ClassName)
        lexer.setColor(QColor("#FFC66D"), QsciLexerPython.FunctionMethodName)
        lexer.setColor(QColor("#BBB529"), QsciLexerPython.Operator)
        lexer.setColor(QColor("#A9B7C6"), QsciLexerPython.Identifier)
        self.setLexer(lexer)

        # behavior
        self.setUtf8(True)
        self.setAutoCompletionSource(QsciScintilla.AutoCompletionSource.AcsAll)
        self.setAutoCompletionThreshold(2)
        self.setWhitespaceVisibility(QsciScintilla.WhitespaceVisibility.WsInvisible)