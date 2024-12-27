from db_setup import initialize_database
from db_test import test_insert_data, test_query_data
from db_operations import clear_database

if __name__ == "__main__":
    initialize_database()
    test_insert_data()

    test_query_data()
    clear_database()
