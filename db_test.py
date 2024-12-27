from db_operations import insert_habit, insert_progress, fetch_all_habits, fetch_progress

def test_insert_data():
    print("Inserting habits...")
    insert_habit("Read", "Daily", 15, "2024-01-01")
    insert_habit("Exercise", "Daily", 30, "2024-01-01")
    print("Habits inserted.")

    print("Inserting progress...")
    insert_progress(1, "2024-01-02", 1)
    insert_progress(2, "2024-01-02", 0)
    print("Progress inserted.")

def test_query_data():
    habits = fetch_all_habits()
    print("Habits:", habits)

    progress = fetch_progress(1)
    print("Progress for Habit ID 1:", progress)

