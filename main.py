from db_setup import initialize_database
from db_test import test_insert_data
from ui import HabitTracker
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    initialize_database()
    test_insert_data()

    app = QApplication(sys.argv)
    window = HabitTracker()
    window.show()
    sys.exit(app.exec_())
    
