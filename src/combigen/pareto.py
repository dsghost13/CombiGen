from PyQt6.QtCore import pyqtSignal, Qt, QPoint, QSize
from PyQt6.QtGui import QColor, QPainter, QPen, QPolygon
from PyQt6.QtWidgets import QGridLayout, QHBoxLayout, QVBoxLayout
from PyQt6.QtWidgets import QComboBox, QLabel, QListView, QPushButton, QWidget

from combigen.reactant import AddButton, DeleteButton
from config.constants import COLORS as C
from config.constants import F, P
from scriptgen.data_fields import TextEntryHandler
from config.stylesheet import dropdown_ss, pareto_axis_ss, pareto_cell_ss, section_ss


class ParetoWidget(QWidget):
    def __init__(self):
        super().__init__()

        pareto_label = QLabel("PARETO FRONT")
        pareto_label.setSizePolicy(P, F)

        add_button = AddButton("Pareto Front")
        add_button.clicked.connect(self.add_pareto_front)

        # Pareto fronts
        self.paretos_layout = QVBoxLayout()
        self.paretos_layout.setContentsMargins(0, 0, 0, 0)
        self.paretos_layout.setSpacing(0)

        paretos_widget = QWidget()
        paretos_widget.setLayout(self.paretos_layout)

        # label + Pareto fronts + button
        module_layout = QVBoxLayout()
        module_layout.addWidget(pareto_label)
        module_layout.addWidget(paretos_widget)
        module_layout.addWidget(add_button)
        self.setLayout(module_layout)

        # bypass style sheet issues when inheriting from QWidget
        wrapper_widget = QWidget()
        wrapper_widget.setLayout(module_layout)
        wrapper_widget.setSizePolicy(P, F)
        wrapper_widget.setStyleSheet(section_ss)

        wrapper_layout = QVBoxLayout()
        wrapper_layout.addWidget(wrapper_widget)
        self.setLayout(wrapper_layout)

    def add_pareto_front(self):
        row_dropdown = AxisDropdown("Row")
        col_dropdown = AxisDropdown("Column")
        del_button = DeleteButton()

        table_widget = TableWidget(row_dropdown, col_dropdown)
        TextEntryHandler.DATA["pareto_fronts"].append(table_widget)

        # button + table
        item_layout = QHBoxLayout()
        item_layout.addWidget(del_button, alignment=Qt.AlignmentFlag.AlignTop)
        item_layout.addWidget(table_widget)

        item_widget = QWidget()
        item_widget.setLayout(item_layout)

        # dropdowns + button + table
        pareto_layout = QVBoxLayout()
        pareto_layout.addWidget(row_dropdown)
        pareto_layout.addWidget(col_dropdown)
        pareto_layout.addWidget(item_widget)

        pareto_widget = QWidget()
        pareto_widget.setLayout(pareto_layout)
        self.paretos_layout.addWidget(pareto_widget)

        # event bindings
        row_dropdown.dropdown.currentIndexChanged.connect(table_widget.update_table)
        col_dropdown.dropdown.currentIndexChanged.connect(table_widget.update_table)
        del_button.clicked.connect(lambda: self.delete_pareto_front(pareto_widget, table_widget))

    def delete_pareto_front(self, pareto_widget, table_widget):
        for i, pf in enumerate(TextEntryHandler.DATA["pareto_fronts"]):
            if pf is table_widget:
                del TextEntryHandler.DATA["pareto_fronts"][i]
        self.paretos_layout.removeWidget(pareto_widget)


class AxisDropdown(QWidget):
    def __init__(self, axis_type):
        super().__init__()

        axis_label = QLabel(f"{axis_type}s: ")
        axis_label.setSizePolicy(F, F)

        self.dropdown = DropdownBox()
        self.dropdown.setFixedWidth(300)
        self.dropdown.setStyleSheet(dropdown_ss)

        axis_layout = QHBoxLayout()
        axis_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        axis_layout.addWidget(axis_label)
        axis_layout.addWidget(self.dropdown)
        self.setLayout(axis_layout)


class TableWidget(QWidget):
    def __init__(self, row_dropdown, col_dropdown):
        super().__init__()
        self.row_select = row_dropdown.dropdown
        self.col_select = col_dropdown.dropdown
        self.row_subs = []
        self.col_subs = []
        self.drag_enabled = False
        self.last_cell = None
        self.placeholder_label = QLabel("...")

        self.table_layout = QGridLayout()
        self.table_layout.addWidget(self.placeholder_label, 0, 0)
        self.table_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.table_layout.setContentsMargins(0, 0, 0, 0)
        self.table_layout.setSpacing(0)
        self.setLayout(self.table_layout)

    def mouseMoveEvent(self, event):
        if self.drag_enabled:
            cell = self.childAt(event.position().toPoint())
            if isinstance(cell, CellButton) and cell is not self.last_cell:
                cell.click()
                self.last_cell = cell

    def update_table(self):
        self.clear()
        self.update_subs()
        if not (self.row_subs == [''] or self.col_subs == ['']):
            self.create_body()
            self.create_row_axis()
            self.create_column_axis()
            self.create_table_toggle()
        else:
            self.table_layout.addWidget(self.placeholder_label, 0, 0)

    def clear(self):
        while self.table_layout.count():
            cell_button = self.table_layout.itemAt(0).widget()
            self.table_layout.removeWidget(cell_button)

    def update_subs(self):
        self.row_subs = TextEntryHandler.parse_text(self.row_select.currentText())
        self.col_subs = TextEntryHandler.parse_text(self.col_select.currentText())

    def create_body(self):
        for i in range(1, len(self.row_subs) + 1):
            for j in range(1, len(self.col_subs) + 1):
                cell_button = CellButton()
                cell_button.setStyleSheet(pareto_cell_ss)
                self.table_layout.addWidget(cell_button, i, j)

    def create_row_axis(self):
        for i in range(1, len(self.row_subs) + 1):
            row_button = CellButton(self.row_subs[i - 1])
            row_button.setStyleSheet(pareto_axis_ss)
            row_button.clicked.connect(lambda checked, row=i: self.toggle_row(row))
            self.table_layout.addWidget(row_button, i, 0)

    def create_column_axis(self):
        for j in range(1, len(self.col_subs) + 1):
            col_button = CellButton(self.col_subs[j - 1])
            col_button.setStyleSheet(pareto_axis_ss)
            col_button.clicked.connect(lambda checked, col=j: self.toggle_column(col))
            self.table_layout.addWidget(col_button, 0, j)

    def create_table_toggle(self):
        table_toggle = TableToggle()
        table_toggle.toggledOn.connect(lambda: self.toggle_table(True))
        table_toggle.toggledOff.connect(lambda: self.toggle_table(False))
        self.table_layout.addWidget(table_toggle, 0, 0)

    def toggle_row(self, i: int):
        for j in range(1, len(self.col_subs) + 1):
            cell_button = self.table_layout.itemAtPosition(i, j).widget()
            cell_button.click()

    def toggle_column(self, j: int):
        for i in range(1, len(self.row_subs) + 1):
            cell_button = self.table_layout.itemAtPosition(i, j).widget()
            cell_button.click()

    def toggle_table(self, state: bool):
        for i in range(1, len(self.row_subs) + 1):
            for j in range(1, len(self.col_subs) + 1):
                cell_button = self.table_layout.itemAtPosition(i, j).widget()
                cell_button.setChecked(state)


class DropdownBox(QComboBox):
    def __init__(self):
        super().__init__()
        view = QListView(self)
        view.setTextElideMode(Qt.TextElideMode.ElideRight)
        self.setView(view)

    def showPopup(self):
        self.update_dropdown()
        super().showPopup()

    def update_dropdown(self):
        pareto_options = TextEntryHandler.RAW["source_subs"] + TextEntryHandler.RAW["sink_subs"]
        pareto_options = [''] if len(pareto_options) == 0 else pareto_options

        current_text = self.currentText()
        current_items = [self.itemText(i) for i in range(self.count())]
        if current_items != pareto_options:
            self.clear()
            self.addItems(pareto_options)

            index = self.findText(current_text)
            if index != -1:
                self.setCurrentIndex(index)
            else:
                self.setCurrentIndex(-1)

    def wheelEvent(self, event):
        event.ignore()


class CellButton(QPushButton):
    def __init__(self, text=''):
        super().__init__()
        self.setCheckable(True)
        self.setChecked(True)
        self.setMouseTracking(True)
        self.setSizePolicy(P, P)
        self.setText(text)

    def sizeHint(self):
        width = self.fontMetrics().horizontalAdvance(self.text()) + 50
        return QSize(width, 50)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.parent().drag_enabled = True
            self.parent().last_cell = self
            self.click()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.parent().drag_enabled = False
            self.releaseMouse()


class TableToggle(QWidget):
    toggledOn = pyqtSignal()
    toggledOff = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        self.setSizePolicy(P, P)

        self.hover_on = False
        self.hover_off = False

    def enterEvent(self, event):
        self.update()

    def leaveEvent(self, event):
        self.hover_on = False
        self.hover_off = False
        self.update()

    def mouseMoveEvent(self, event):
        x = event.position().x()
        y = event.position().y()

        self.hover_on = (x / self.width() + y / self.height()) < 1
        self.hover_off = (x / self.width() + y / self.height()) > 1
        self.update()

    def mousePressEvent(self, event):
        if event.button() != Qt.MouseButton.LeftButton:
            return

        x = event.position().x()
        y = event.position().y()

        if (x / self.width() + y / self.height()) < 1:
            self.toggledOn.emit()
        else:
            self.toggledOff.emit()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)

        w = self.width()
        h = self.height()

        # on button
        on_button = QPolygon([
            QPoint(0, 0),
            QPoint(w, 0),
            QPoint(0, h)
        ])
        on_color = QColor(C["LIGHT_GREEN"]) if self.hover_on else QColor(C["DARK_GREEN"])
        painter.setBrush(on_color)
        painter.drawPolygon(on_button)

        # off button
        off_button = QPolygon([
            QPoint(w, h),
            QPoint(w, 0),
            QPoint(0, h)
        ])
        off_color = QColor(C["LIGHT_RED"]) if self.hover_off else QColor(C["DARK_RED"])
        painter.setBrush(off_color)
        painter.drawPolygon(off_button)

        # diagonal line and border
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(Qt.GlobalColor.white, 1))
        painter.drawLine(0, h, w, 0)
        painter.drawRect(0, 0, w, h)