import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QDialog,
    QLabel,
    QLineEdit,
    QFormLayout,
    QMessageBox,
    QHeaderView,
)

from PyQt5.QtGui import QFont

from db_operations import (
    fetch_all_habits,
    insert_habit,
)


class HabitTracker(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Habit Tracker")
        self.setMinimumSize(800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.habit_table = QTableWidget()
        self.habit_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                gridline-color: #d0d0d0;
                border: 1px solid #c0c0c0;
                border-radius: 4px;
            }
            QHeaderView::section {
                background-color: #2c3e50;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 10px;
                border: none;
                color: black
            }
        """)
        self.habit_table.setAlternatingRowColors(True)
        self.habit_table.horizontalHeader().setStretchLastSection(True)
        self.habit_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Interactive
        )
        self.habit_table.verticalHeader().setVisible(False)
        self.habit_table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        self.habit_table.setColumnCount(4)
        self.habit_table.setHorizontalHeaderLabels(
            ["ID", "Name", "Frequency", "Goal"]
        )
        self.layout.addWidget(self.habit_table)

        button_layout = QHBoxLayout()
        self.add_habit_button = QPushButton("Add Habit")
        self.remove_habit_button = QPushButton("Remove Habit")
        self.edit_habit_button = QPushButton("Edit Habit")
        button_style = """
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #2070a9;
            }
        """
        self.add_habit_button.setStyleSheet(button_style)
        self.edit_habit_button.setStyleSheet(button_style)
        self.remove_habit_button.setStyleSheet(
            button_style.replace("#3498db", "#e74c3c")
        )

        button_layout.addWidget(self.add_habit_button)
        button_layout.addWidget(self.edit_habit_button)
        button_layout.addWidget(self.remove_habit_button)
        self.layout.addLayout(button_layout)

        self.layout.setSpacing(20)
        self.layout.setContentsMargins(20, 20, 20, 20)
        button_layout.setSpacing(10)

        app_font = QFont("Segoe UI", 10)
        self.setFont(app_font)

        self.add_habit_button.clicked.connect(self.open_add_habit_dialog)
        self.remove_habit_button.clicked.connect(self.delete_selected_habit)

        # Load Habits
        self.load_habits()

    def load_habits(self):
        self.habit_table.setRowCount(0)
        habits = fetch_all_habits()

        for row_num, habit in enumerate(habits):
            self.habit_table.insertRow(row_num)
            for col_num, data in enumerate(habit):
                self.habit_table.setItem(
                    row_num, col_num, QTableWidgetItem(str(data))
                )

    def open_add_habit_dialog(self):
        dialog = AddHabitDialog(self)
        dialog.exec_()
        self.load_habits()

    def delete_selected_habit(self):
        """Delete the selected habit."""
        selected_row = self.habit_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "No habit selected!")
            return
        habit_id = self.habit_table.item(selected_row, 0).text()


class AddHabitDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Habit")
        self.setGeometry(300, 300, 400, 300)

        # Form Layout
        self.form_layout = QFormLayout()
        self.setLayout(self.form_layout)

        # Input Fields
        self.name_input = QLineEdit()
        self.frequency_input = QLineEdit()
        self.goal_input = QLineEdit()
        self.start_date_input = QLineEdit()
        self.form_layout.addRow("Habit Name:", self.name_input)
        self.form_layout.addRow(
            "Frequency (e.g., Daily):", self.frequency_input
        )
        self.form_layout.addRow("Goal (Minutes):", self.goal_input)
        self.form_layout.addRow(
            "Start Date (YYYY-MM-DD):", self.start_date_input
        )

        # Buttons
        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        self.form_layout.addRow(button_layout)

        # Connect Buttons
        self.save_button.clicked.connect(self.save_habit)
        self.cancel_button.clicked.connect(self.reject)

    def save_habit(self):
        """Save habit to the database."""
        name = self.name_input.text()
        frequency = self.frequency_input.text()
        goal = self.goal_input.text()
        start_date = self.start_date_input.text()

        if not (name and frequency and goal and start_date):
            QMessageBox.warning(self, "Error", "All fields are required!")
            return

        try:
            insert_habit(name, frequency, int(goal), start_date)
            QMessageBox.information(
                self, "Success", "Habit added successfully!"
            )
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add habit: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HabitTracker()
    window.show()
    sys.exit(app.exec_())
