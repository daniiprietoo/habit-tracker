import sqlite3

DB_PATH = "db/habits.db"


def insert_habit(name, frequency, goal, start_date):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
    INSERT INTO habits (name, frequency, goal, start_date)
    VALUES (?, ?, ?, ?)
  """,
        (name, frequency, goal, start_date),
    )

    conn.commit()
    conn.close()


def insert_progress(habit_id, date, status):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
    INSERT INTO progress (habit_id, date, status)
    VALUES (?, ?, ?)
    """,
        (habit_id, date, status),
    )

    conn.commit()
    conn.close()


def fetch_all_habits():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM habits
  """)

    habits = cursor.fetchall()
    conn.close()
    return habits


def fetch_habit_by_id(habit_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
    SELECT * FROM habits WHERE id = ?
""",
    (habit_id,),
)

    habit = cursor.fetchone()
    conn.close()
    return habit


def fetch_progress(habit_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
      SELECT * FROM progress WHERE habit_ID = ?
    """,
        (habit_id,),
    )

    progress = cursor.fetchall()
    conn.close()

    return progress


def clear_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM habits
  """)

    cursor.execute("""
    DELETE FROM progress
  """)

    conn.commit()
    conn.close()

    print("Database cleared")

def delete_habit(habit_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
    DELETE FROM habits WHERE id = ?
  """,
        (habit_id,),
    )

    cursor.execute(
        """
    DELETE FROM progress WHERE habit_id = ?
  """,
        (habit_id,),
    )

    conn.commit()
    conn.close()

def update_habit_by_id(habit_id, name, frequency, goal, start_date):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
    UPDATE habits
    SET name = ?, frequency = ?, goal = ?, start_date = ?
    WHERE id = ?
  """,
        (name, frequency, goal, start_date, habit_id),
    )

    conn.commit()
    conn.close()