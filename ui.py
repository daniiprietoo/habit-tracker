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
    QLineEdit,
    QFormLayout,
    QMessageBox,
    QHeaderView,
    QLabel,
    QCalendarWidget,
    QComboBox,
    QSpinBox,
    QFrame,
)
from PyQt5.QtGui import QFont, QIcon, QColor
from PyQt5.QtCore import Qt, QSize
from db_operations import (
    fetch_all_habits,
    insert_habit,
    delete_habit,
    fetch_habit_by_id,
    update_habit_by_id,
)


class HabitTracker(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("✨ Habit Tracker")
        self.setMinimumSize(900, 700)

        self.colors = {
            'primary': '#2962ff',
            'secondary': '#455a64',
            'danger': '#f44336',
            'success': '#4caf50',
            'background': '#f5f5f5',
            'surface': '#ffffff',
            'text': '#263238' 
        }

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget.setStyleSheet(f"background-color: {self.colors['background']}")

        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setSpacing(24)
        main_layout.setContentsMargins(32, 32, 32, 32)

        header_layout = QHBoxLayout()
        header_label = QLabel("My Habits")
        header_label.setStyleSheet(f"""
            QLabel {{
                color: {self.colors['text']};
                font-size: 24px;
                font-weight: bold;
            }}
        """)
        header_layout.addWidget(header_label)
        header_layout.addStretch()
        main_layout.addLayout(header_layout)


        stats_layout = QHBoxLayout()
        self.create_stat_card("Total Habits", "0", stats_layout)
        self.create_stat_card("Active Streaks", "0", stats_layout)
        self.create_stat_card("Completed Today", "0", stats_layout)
        main_layout.addLayout(stats_layout)


        self.habit_table = QTableWidget()
        self.setup_table()
        main_layout.addWidget(self.habit_table)

        button_layout = QHBoxLayout()
        self.setup_buttons(button_layout)
        main_layout.addLayout(button_layout)

        app_font = QFont("Segoe UI", 10)
        self.setFont(app_font)
    

        self.add_habit_button.clicked.connect(self.open_add_habit_dialog)
        self.remove_habit_button.clicked.connect(self.delete_selected_habit)
        self.edit_habit_button.clicked.connect(self.open_edit_habit_dialog)

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
        selected_row = self.habit_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "No habit selected!")
            return
        habit_id = self.habit_table.item(selected_row, 0).text()
        delete_habit(habit_id)
        self.load_habits()

    def open_edit_habit_dialog(self):
        selected_row = self.habit_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "No habit selected!")
            return
        habit_id = self.habit_table.item(selected_row, 0).text()
        dialog = EditHabitDialog(habit_id, self)
        dialog.exec_()
        self.load_habits()

    def create_stat_card(self, title, value, parent_layout):
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {self.colors['surface']};
                border-radius: 10px;
                padding: 16px;
                margin: 8px;
            }}
        """)

        card_layout = QVBoxLayout(card)
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #757575; font-size: 14px;")
        value_label = QLabel(value)
        value_label.setStyleSheet("color: #212121; font-size: 24px; font-weight: bold;")
        
        card_layout.addWidget(title_label)
        card_layout.addWidget(value_label)
        parent_layout.addWidget(card) 

    def setup_table(self):
        self.habit_table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {self.colors['surface']};
                gridline-color: #e0e0e0;
                border: none;
                border-radius: 8px;
            }}
            QHeaderView::section {{
                background-color: {self.colors['surface']};
                color: {self.colors['text']};
                padding: 12px;
                border: none;
                font-weight: bold;
                border-bottom: 2px solid #e0e0e0;
            }}
            QTableWidget::item {{
                padding: 12px;
                border-bottom: 1px solid #f0f0f0;
            }}
            QTableWidget::item:selected {{
                background-color: {self.colors['primary'] + '22'};
                color: {self.colors['text']};
            }}
        """)

        self.habit_table.setAlternatingRowColors(True)
        self.habit_table.horizontalHeader().setStretchLastSection(True)
        self.habit_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.habit_table.verticalHeader().setVisible(False)
        self.habit_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.habit_table.setColumnCount(5)
        self.habit_table.setHorizontalHeaderLabels(["ID", "📝 Habit", "🔁 Frequency", "🎯 Goal", "🗓️ Start Date"])
    
    def setup_buttons(self, button_layout):
        button_base_style = """
            QPushButton {{
                background-color: {};
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {};
            }}
            QPushButton:pressed {{
                background-color: {};
            }}
        """

        self.add_habit_button = QPushButton("➕ Add Habit")
        self.edit_habit_button = QPushButton("📝 Edit Habit")
        self.remove_habit_button = QPushButton("🗑️ Remove Habit")

        self.add_habit_button.setStyleSheet(button_base_style.format(self.colors['primary'], '#1976d2', '#1565c0'))
        self.edit_habit_button.setStyleSheet(button_base_style.format(self.colors['secondary'], '#37474f', '#263238'))
        self.remove_habit_button.setStyleSheet(button_base_style.format(self.colors['danger'], '#d32f2f', '#c62828'))

        button_layout.addWidget(self.add_habit_button)
        button_layout.addWidget(self.edit_habit_button)
        button_layout.addWidget(self.remove_habit_button)
        button_layout.setSpacing(12)

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


class EditHabitDialog(QDialog):
    def __init__(self, habit_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Habit")
        self.setGeometry(300, 300, 400, 300)
        self.habit_id = habit_id
        self.habit = fetch_habit_by_id(habit_id)

        self.form_layout = QFormLayout()
        self.setLayout(self.form_layout)

        self.name_input = QLineEdit()
        self.name_input.setText(self.habit[1])
        self.frequency_input = QLineEdit()
        self.frequency_input.setText(self.habit[2])
        self.goal_input = QLineEdit()
        self.goal_input.setText(str(self.habit[3]))
        self.start_date_input = QLineEdit()
        self.start_date_input.setText(self.habit[4])

        self.form_layout.addRow("Habit Name:", self.name_input)
        self.form_layout.addRow(
            "Frequency (e.g., Daily):", self.frequency_input
        )
        self.form_layout.addRow("Goal (Minutes):", self.goal_input)
        self.form_layout.addRow(
            "Start Date (YYYY-MM-DD):", self.start_date_input
        )

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_habit)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)

        self.form_layout.addRow(button_layout)

    def save_habit(self):
        name = self.name_input.text()
        frequency = self.frequency_input.text()
        goal = self.goal_input.text()
        start_date = self.start_date_input.text()

        if not (name and frequency and goal and start_date):
            QMessageBox.warning(self, "Error", "All fields are required!")
            return

        try:
            update_habit_by_id(
                self.habit_id, name, frequency, int(goal), start_date
            )
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
